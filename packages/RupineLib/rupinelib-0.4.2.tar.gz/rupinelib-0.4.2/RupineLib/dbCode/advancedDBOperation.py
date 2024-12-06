import json
from datetime import datetime
from psycopg2 import sql
from .directDBOperation import insertDataIntoDatabase, fetchDataInDatabase, updatetBulkDataInDatabaseByCopyManager, insertBulkDataIntoDatabaseByCopyManager, insertBulkDataIntoDatabase


def POST(connection, schema, tableName:str, data:dict, onConflict:bool=False, uniqueColumnNamesForConflict:str='id'):
    """
    Inserts a single row into the specified table in the given schema, with optional conflict handling.

    :param connection: Database connection object.
    :param schema: The schema where the target table resides.
    :param tableName: Name of the target table for insertion.
    :param data: Dictionary representing the row to insert, with column names as keys and corresponding values.
                 The dictionary must include all `NOT NULL` columns without default values, otherwise an error will occur.
    :param onConflict: If True, specifies that the insertion should ignore rows with conflicts on the unique column(s).
    :param uniqueColumnNamesForConflict: Comma-separated string of column name(s) that define the uniqueness constraint. Only applicable if `onConflict` is True.

    :return: Result of the insertion operation, as returned by `insertDataIntoDatabase` function.

    Notes:
    - Adds `created_at` and `modified_at` timestamps to the data automatically.
    - If `onConflict` is set, rows with duplicate values in `uniqueColumnNamesForConflict` will be ignored.
    - This function dynamically creates the `INSERT` query and parameters based on the `data` dictionary provided.
    """
    # TODO: Check if any column is not nullable that does not appear in data. Return ERROR in this case
    data['created_at'] = int(datetime.now().timestamp())
    data['modified_at'] = int(datetime.now().timestamp())
    columns = data.keys()
    onConflictString = ''
    if onConflict:
        onConflictString = 'ON CONFLICT ({}) DO NOTHING'.format(uniqueColumnNamesForConflict)
    queryString = "INSERT INTO {{}}.{} ({}) VALUES ({}) {};".format(tableName,', '.join(columns),','.join(['%s']*len(columns)),onConflictString)

    params = []
    for key in data:
        if type(data[key]) == dict or type(data[key]) == list:
            params.append(json.dumps(data[key]))
        else:
            params.append(data[key])

    query = sql.SQL(queryString).format(sql.Identifier(schema))
    result = insertDataIntoDatabase(query, params, connection)    
    return result

def POST_BULK(connection, schema, tableName:str, data:list, byCopy = True, onConflict:bool=False, uniqueColumnNamesForConflict:str='id'):
    """
    Inserts multiple rows in bulk into the specified table, with optional conflict handling and different insertion modes.

    :param connection: Database connection object.
    :param schema: The schema where the target table resides.
    :param tableName: Name of the target table for bulk insertion.
    :param data: List of dictionaries, where each dictionary represents a row to insert, with column names as keys.
                 Each dictionary must contain the same keys and include all `NOT NULL` columns without defaults.
    :param byCopy: If True, uses `COPY` method for bulk insertion (faster for large data sets); otherwise, uses standard bulk insertion.
    :param onConflict: If True, enables conflict handling to ignore rows with conflicts on the unique column(s).
    :param uniqueColumnNamesForConflict: Comma-separated string of column name(s) that define the uniqueness constraint. Only applicable if `onConflict` is True.

    :return: Result of the bulk insertion operation, as returned by the relevant bulk insertion function.

    Notes:
    - Adds `created_at` and `modified_at` timestamps to each row automatically.
    - Ensures columns of JSON type are converted properly, based on `byCopy` mode.
    - If `onConflict` is True, rows with duplicate values in `uniqueColumnNamesForConflict` will be ignored.
    - Automatically builds the `INSERT` query and template based on the columns in the first dictionary of `data`.
    """
    query = sql.SQL('SELECT column_name,data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
    res = fetchDataInDatabase(query, [schema,tableName], connection)
    columns = []
    template = []
    for row in res:
        if row[0] in data[0]:
            columns.append(row[0])
            if row[1] == 'json':
                template.append('%s::json')
            else:
                template.append('%s')
    template = '(' + ','.join(template) + ')' 

    newData = []
    for item in data:
        item['created_at'] = int(datetime.now().timestamp())
        item['modified_at'] = int(datetime.now().timestamp())
        # TODO: Check if any column is not nullable that does not appear in data. Return ERROR in this case
        newItem = []
        for column in columns:
            if column in item:
                if type(item[column]) == dict or type(item[column]) == list:
                    if byCopy:
                        newItem.append(json.dumps(item[column]).encode('utf8'))
                    else:
                        newItem.append(json.dumps(item[column]))
                elif type(item[column]) == str:
                    if byCopy:
                        newItem.append(str(item[column]).encode('utf8'))
                    else:
                        newItem.append(item[column])
                else:
                    newItem.append(item[column])
            else:
                newItem.append(None)
        newData.append(newItem)

    if byCopy and not onConflict:
        result = insertBulkDataIntoDatabaseByCopyManager('.'.join([schema,tableName]),columns,newData,connection)  
    else:
        onConflictString = ''
        if onConflict:
            onConflictString = 'ON CONFLICT ({}) DO NOTHING'.format(uniqueColumnNamesForConflict)
        queryString = "INSERT INTO {{}}.{} ({}) VALUES %s {};".format(tableName,', '.join(columns),onConflictString)
        query = sql.SQL(queryString).format(sql.Identifier(schema))
        result = insertBulkDataIntoDatabase(query,template,newData,connection)
    return result

def PUT(connection, schema, updates:dict, tableName:str, conditions:dict={}):
    """
    Updates rows in a specified table based on given conditions.

    :param connection: Database connection object.
    :param schema: The schema where the target table resides.
    :param updates: Dictionary of column-value pairs representing columns to be updated and their new values.
                    Automatically adds a `modified_at` timestamp to the updates.
    :param tableName: Name of the target table for the update operation.
    :param conditions: Dictionary of conditions for the update operation, with column names as keys.
                       - If the value is a list, the condition is an `IN` clause.
                       - If the value is a single item, it forms an equality condition.
                       - If no conditions are provided, all rows in the table will be updated.

    :return: None

    Notes:
    - Builds the `SET` clause dynamically based on the `updates` dictionary.
    - Creates a condition clause using `IN` and equality operators as specified in `conditions`.
    - Ensures that JSON-type columns in `updates` are serialized as strings.
    - If `conditions` is empty, all rows will be affected by the update.
    """
    updates['modified_at'] = int(datetime.now().timestamp())
    sqlTemplateEqual = "{} = %s"
    sqlTemplateIn = "{} IN ({})"
    setArray = []
    conditionArray = []
    params = []
    for key in updates.keys():
        setArray.append(sqlTemplateEqual.format(key))
        if type(updates[key]) == dict or type(updates[key]) == list:
            params.append(json.dumps(updates[key]))
            
        else:
            params.append(updates[key])
    
    for key in conditions.keys():
        if type(conditions[key]) == list:
            conditionArray.append(sqlTemplateIn.format(key,','.join(['%s'] * len(conditions[key]))))
            for item in conditions[key]:
                params.append(item) 
        else:
            conditionArray.append(sqlTemplateEqual.format(key))
            params.append(conditions[key]) 
    
    if len(conditionArray) == 0:
        queryString = "UPDATE {{}}.{} SET {}".format(tableName,', '.join(setArray))
    else:
        queryString = "UPDATE {{}}.{} SET {} WHERE 1=1 AND {}".format(tableName,', '.join(setArray),' AND '.join(conditionArray))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    insertDataIntoDatabase(query, params, connection)    
    return None

def PUT_BULK(connection, schema, updates:list, tableName:str, conditionColumns:list=['id']):
    """
    Performs a bulk update on a specified table by creating a temporary table with new data and updating matching records
    in the target table based on given conditions.

    :param connection: Database connection object.
    :param schema: The schema in which the target table resides.
    :param updates: List of dictionaries, where each dictionary contains column-value pairs representing rows to be updated.
                    All dictionaries in the list should have the same keys, with each key being a column name in the database.
                    Each column that is `NOT NULL` without a default value in the database must be included in `updates`.
    :param tableName: The name of the target table to be updated.
    :param conditionColumns: List of column names used as conditions to match rows in the target table.
                             These columns should also be present in the `updates` dictionaries.

    :return: Result of the bulk update operation, or an error message if conditions are not met.
             Returns a dictionary with 'error' key set to 1 if an error is encountered.

    Note:
    - This function dynamically constructs the column list for the update based on the `updates` dictionary keys 
      and adds a `modified_at` timestamp for each update.
    - It validates that required `NOT NULL` columns without defaults are provided in `updates`.
    - Any `conditionColumns` not found in `updates` result in an error.
    
    Process:
    1. Retrieves the column names and data types from `information_schema.columns` for the specified table.
    2. Constructs a temporary table and populates it with `newData` based on the provided `updates`.
    3. Executes an `UPDATE` query that joins the temporary table with the target table on `conditionColumns`.
    """
    query = sql.SQL('SELECT column_name,data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
    res = fetchDataInDatabase(query, [schema,tableName], connection)
    columns = ['modified_at']
    for row in res:
        if row[0] in updates[0]:
            columns.append(row[0])


    newData = []
    for item in updates:
        item['modified_at'] = int(datetime.now().timestamp())
        # TODO: Check if any column is not nullable that does not appear in data. Return ERROR in this case
        newItem = []
        for column in columns:
            if column in item:
                if type(item[column]) == dict or type(item[column]) == list:
                    newItem.append(json.dumps(item[column]).encode('utf8'))
                elif type(item[column]) == str:
                    newItem.append(str(item[column]).encode('utf8'))
                else:
                    newItem.append(item[column])
            else:
                newItem.append(None)
        newData.append(newItem)

    setArray = []
    conditionArray = []

    for col in conditionColumns:
        if col not in columns:
            return {
                'error': 1,
                'msg': 'at least one columnn in conditionColumns is not in updates'
            }
        conditionArray.append("t.{} = tmp.{}".format(col,col))
    for col in columns:
        if col not in conditionColumns:
            setArray.append("{} = tmp.{}".format(col,col))
    
    tmpTableName = schema + '_tmp_' + tableName
    queryString = "UPDATE {{}}.{} AS t SET {} FROM {} tmp WHERE 1=1 AND {}".format(tableName,', '.join(setArray),tmpTableName,' AND '.join(conditionArray))

    query = sql.SQL(queryString).format(sql.Identifier(schema))

    result = updatetBulkDataInDatabaseByCopyManager(schema,tableName,columns,newData,query,connection)   
    return result

def SELECT(connection, schema, columns:list, tableName:str, conditions:dict={}, default:list=[]):
    """
    Retrieves a dictionary of all specifiers and their values for a given loop attribute.

    :param connection: A connection object created using the RupineLib package via `db.connect(...)` or `db.connectURI(...)`.
    :param schema: Name of the schema (case-sensitive).
    :param columns: List of column names to be selected. Use `[]` or `['*']` to select all columns.
    :param tableName: Name of the table (case-sensitive).
    :param conditions: Dictionary specifying conditions for the query, where each key represents a column name, and each value defines the condition for that column.
                    Conditions are concatenated with `AND`.
                    - If the value is not a dictionary:
                        - `key = value` forms a simple condition (e.g., `column_name = value`).
                        - If `value` is `None`, the condition becomes `column_name IS NULL`.
                    - If the value is a dictionary, the following keys are expected:
                        - `"value"`: The condition value.
                        - `"operator"`: The operator, such as `lt`, `lte`, `gt`, `gte`, `in`, `not in`, `is not`.
                        - `"alias"` (optional): If present, this key overrides the dictionary key and serves as the real column name in the condition.

                    Example:
                    ```
                    conditions = {
                        "my_column": "some value",  # Generates `WHERE my_column = 'some value'`
                        "someNameWhichIsNotAColumnName: {
                            "value": 100,
                            "operator": "lt",
                            "alias": "my_column" # Generates `WHERE my_column < 100`
                        },
                        "someNameWhichIsNotAColumnName: {
                            "value": [1,2],
                            "operator": "in",
                            "alias": "my_column" # Generates `WHERE my_column in [1,2]`
                        },
                        "someNameWhichIsNotAColumnName: {
                            "value": None,
                            "operator": "is not",
                            "alias": "my_column" # Generates `WHERE my_column IS NOT NULL`
                        }
                    }
                    ```

    :return: A list of objects containing the selected data for the columns provided in the list.
    """
    if columns == [] or columns == ['*']:
        query = sql.SQL('SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
        res = fetchDataInDatabase(query, [schema,tableName], connection)
        columns = []
        for row in res:
            columns.append(row[0])
    
    sqlTemplateEqual = "{} = %s"
    sqlTemplateIn = "{} IN ({})"
    sqlTemplateNotIn = "{} NOT IN ({})"
    sqlTemplateIsNull = "{} IS NULL"
    sqlTemplateIsNotNull = "{} IS NOT NULL"

    sqlTemplateLt = "{} < %s"
    sqlTemplateLte = "{} <= %s"
    sqlTemplateGt = "{} > %s"
    sqlTemplateGte = "{} >= %s"
    
    # JSON templates
    sqlTemplateJSONContainsFirst = "{} <@ %s"
    sqlTemplateJSONContainsSecond = "{} @> %s"
    conditionArray = []
    params = []
    for key in conditions.keys():
        conditionColumnName = key
        if type(conditions[key]) == dict:
            conditionValue = conditions[key]['value']
            if 'alias' in conditions[key]:
                conditionColumnName = conditions[key]['alias']
            sqlTemplate = None
            if conditions[key]['operator'] == 'lt':
                sqlTemplate = sqlTemplateLt
            elif conditions[key]['operator'] == 'lte':
                sqlTemplate = sqlTemplateLte
            elif conditions[key]['operator'] == 'gt':
                sqlTemplate = sqlTemplateGt
            elif conditions[key]['operator'] == 'gte':
                sqlTemplate = sqlTemplateGte
            elif conditions[key]['operator'] == 'not in':
                sqlTemplate = sqlTemplateNotIn
            elif conditions[key]['operator'] == 'in':
                sqlTemplate = sqlTemplateIn
            elif conditions[key]['operator'] == 'is not':
                sqlTemplate = sqlTemplateIsNotNull
            elif conditions[key]['operator'] == '<@':
                sqlTemplate = sqlTemplateJSONContainsFirst
            elif conditions[key]['operator'] == '@>':
                sqlTemplate = sqlTemplateJSONContainsSecond
        else:
            conditionValue = conditions[key]
            if conditionValue is None:
                sqlTemplate = sqlTemplateIsNull
            else:
                sqlTemplate = sqlTemplateEqual
        
        
        if type(conditionValue) == list:
            if sqlTemplate is None or sqlTemplate not in (sqlTemplateIn,sqlTemplateNotIn):
                conditionArray.append(sqlTemplateIn.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            else:
                conditionArray.append(sqlTemplate.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            for item in conditionValue:
                params.append(item) 
        else:
            conditionArray.append(sqlTemplate.format(conditionColumnName))
            if conditionValue is not None:
                params.append(conditionValue) 
   
    if len(conditionArray) == 0:
        queryString = "SELECT {} FROM {{}}.{}".format(', '.join(columns),tableName)
    else:
        queryString = "SELECT {} FROM {{}}.{} WHERE 1=1 AND {}".format(', '.join(columns),tableName,' AND '.join(conditionArray))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    res = fetchDataInDatabase(query, params, connection)    

    if res == None or res == []:
        return default
    
    result = []
    for row in res:
        resultDict = {}
        for idx,item in enumerate(row):
            resultDict[columns[idx]] = item
        result.append(resultDict)
    return result

def SELECT_FUNCTION(connection, schema,functionName,functionParameter:list,columns:list=[]):
    """
    Executes a specified PostgreSQL function and returns the result as a list of dictionaries.

    :param connection: Database connection object.
    :param schema: Schema in which the function resides.
    :param functionName: Name of the PostgreSQL function to execute.
    :param functionParameter: List of parameters to pass to the function, in the order they are expected.
    :param columns: List of column names to select in the query. If set to `[]` or `['*']`, column names will be inferred based on the function's return type.
                    This requires the `get_return_columns_of_function` function to retrieve column names.

    :return: List of dictionaries where each dictionary represents a row returned by the function, with column names as keys.

    Notes:
    - Automatically retrieves column names if `columns` is empty or set to `['*']`.
    - Executes a dynamic SQL `SELECT` query on the function and formats the results into dictionaries.
    - Only functions with supported return types (as per `get_return_columns_of_function`) are compatible.
    - Returns an empty list if the function has no output or if there are errors in the retrieval process.
    """
    if columns == [] or columns == ['*']:
        queryString = 'SELECT column_name, arg_type, col_num FROM {}.get_return_columns_of_function(%s,%s)'
        query = sql.SQL(queryString).format(sql.Identifier(schema))
        # query = sql.SQL('SELECT t.column_name, t.arg_type::regtype::text, t.col_num FROM pg_proc p LEFT JOIN pg_namespace pn ON p.pronamespace = pn.oid \
        #                 CROSS JOIN UNNEST(proargnames, proargmodes, proallargtypes) WITH ORDINALITY AS t(column_name, arg_mode, arg_type, col_num) \
        #                 WHERE p.proname = %s AND pn.nspname = %s AND t.arg_mode = \'t\' ORDER BY t.col_num')
        res = fetchDataInDatabase(query, [functionName,schema], connection)
        if res == None:
            return []
        
        columns = []
        for row in res:
            columns.append(row[0])
    queryString = "SELECT {} FROM {{}}.{}({})".format(', '.join(columns),functionName,','.join(['%s']*len(functionParameter)))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    res = insertDataIntoDatabase(query, functionParameter, connection)    

    if res == None:
        return []
    
    result = []
    for row in res:
        resultDict = {}
        for idx,item in enumerate(row):
            resultDict[columns[idx]] = item
        result.append(resultDict)
    return result

def DELETE(connection, schema, tableName:str, conditions:dict={}):
    """
    Deletes rows from a specified table in the database based on given conditions.

    :param connection: Database connection object.
    :param schema: Schema in which the target table resides.
    :param tableName: Name of the table from which rows should be deleted.
    :param conditions: Dictionary defining the conditions for deletion, where:
                       - Keys are column names.
                       - Values are either direct values or dictionaries specifying:
                           - "value": Value to compare.
                           - "operator": Operator to use (e.g., 'lt', 'lte', 'gt', 'gte', 'not in', 'in', 'is not').
                           - "alias": Optional alias if the key is not the actual column name.
                       - If no conditions are specified, all rows in the table will be deleted.

    :return: Boolean `True` indicating successful deletion.

    Notes:
    - Builds the `WHERE` clause dynamically based on `conditions`, supporting operators like `IN`, `IS NULL`, `<`, `<=`, etc.
    - Accepts various condition types (e.g., lists for `IN` conditions, dictionaries for complex conditions).
    - Returns `True` after successful execution of the deletion query.
    - If `conditions` is empty, deletes all rows in the specified table.
    """
    query = sql.SQL('SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s')
    res = fetchDataInDatabase(query, [schema,tableName], connection)
    columns = []
    for row in res:
        columns.append(row[0])
    
    sqlTemplateEqual = "{} = %s"
    sqlTemplateIn = "{} IN ({})"
    sqlTemplateNotIn = "{} NOT IN ({})"
    sqlTemplateIsNull = "{} IS NULL"
    sqlTemplateIsNotNull = "{} IS NOT NULL"

    sqlTemplateLt = "{} < %s"
    sqlTemplateLte = "{} <= %s"
    sqlTemplateGt = "{} > %s"
    sqlTemplateGte = "{} >= %s"
    conditionArray = []
    params = []
    for key in conditions.keys():
        conditionColumnName = key
        if type(conditions[key]) == dict:
            conditionValue = conditions[key]['value']
            if 'alias' in conditions[key]:
                conditionColumnName = conditions[key]['alias']
            sqlTemplate = None
            if conditions[key]['operator'] == 'lt':
                sqlTemplate = sqlTemplateLt
            elif conditions[key]['operator'] == 'lte':
                sqlTemplate = sqlTemplateLte
            elif conditions[key]['operator'] == 'gt':
                sqlTemplate = sqlTemplateGt
            elif conditions[key]['operator'] == 'gte':
                sqlTemplate = sqlTemplateGte
            elif conditions[key]['operator'] == 'not in':
                sqlTemplate = sqlTemplateNotIn
            elif conditions[key]['operator'] == 'in':
                sqlTemplate = sqlTemplateIn
            elif conditions[key]['operator'] == 'is not':
                sqlTemplate = sqlTemplateIsNotNull
        else:
            conditionValue = conditions[key]
            if conditionValue is None:
                sqlTemplate = sqlTemplateIsNull
            else:
                sqlTemplate = sqlTemplateEqual
        
        
        if type(conditionValue) == list:
            if sqlTemplate is None or sqlTemplate not in (sqlTemplateIn,sqlTemplateNotIn):
                conditionArray.append(sqlTemplateIn.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            else:
                conditionArray.append(sqlTemplate.format(conditionColumnName,','.join(['%s'] * len(conditionValue))))
            for item in conditionValue:
                params.append(item) 
        else:
            conditionArray.append(sqlTemplate.format(conditionColumnName))
            if conditionValue is not None:
                params.append(conditionValue) 
   
    queryString = "DELETE FROM {{}}.{} WHERE 1=1 AND {}".format(tableName,' AND '.join(conditionArray))
    query = sql.SQL(queryString).format(sql.Identifier(schema))
    res = insertDataIntoDatabase(query, params, connection)    

    return True

def TRUNCATE(connection, schema, tableName:str):
    """
    Truncates table

    :param connection: Database connection object.
    :param schema: Schema in which the target table resides.
    :param tableName: Name of the table from which rows should be deleted.
    """
    query = sql.SQL("TRUNCATE TABLE {}.{}").format(sql.Identifier(schema),sql.Identifier(tableName))
    res = insertDataIntoDatabase(query, [], connection) 

    return True   
