from .dbCode import connection as conn
from .dbCode import directDBOperation as directOP
from .dbCode import advancedDBOperation as advOP

def connect(user,pw,host,Port,database):
    """
    Establishes a PostgreSQL database connection using provided connection details.

    :param user: Username for authenticating with the PostgreSQL database.
    :param pw: Password for the specified user.
    :param host: Database server address (hostname or IP address).
    :param Port: Port number on which the PostgreSQL server is listening.
    :param database: Name of the database to connect to.

    :return: A `psycopg2` connection object that can be used to interact with the specified database.
    
    :raises psycopg2.OperationalError: If the connection cannot be established.

    Notes:
    - Uses SSL mode (`sslmode='require'`) for the connection.
    - Format the connection string securely, and avoid logging or displaying the password.
    """
    return conn.connect(user,pw,host,Port,database)

def connectURI(connectionStr):
    """
    Establishes a PostgreSQL database connection using a full URI string.

    :param connectionStr: Full PostgreSQL URI string formatted as 
                          "postgres://username:password@host:port/database".
                          
    :return: A `psycopg2` connection object that can be used to interact with the specified database.
    
    :raises psycopg2.OperationalError: If the connection cannot be established.

    Notes:
    - Uses SSL mode (`sslmode='require'`) for secure connection.
    - The URI string must include all required connection parameters.
    """
    return conn.connectURI(connectionStr)

def fetchDataInDatabase(sql:str, params:list, connection):
    """
    Executes a SQL query and fetches all results.

    :param sql: SQL query string to execute.
    :param params: List of parameters to pass to the SQL query.
    :param connection: Active database connection object.

    :return: List of tuples representing rows returned by the query.

    Notes:
    - This method is designed to fetch all results of a query.
    - Handles any exceptions by returning the exception object, allowing the caller to handle the error.
    """
    return directOP.fetchDataInDatabase(sql,params,connection)

def insertDataIntoDatabase(sql:str, params:list, connection):  
    """
    Inserts data into the database and fetches any returned results.

    :param sql: SQL query string to execute, expected to be an INSERT statement.
    :param params: List of parameters to pass to the SQL query.
    :param connection: Active database connection object.

    :return: List of tuples with any returned rows from the executed SQL query, or `None` if no rows are returned.
             Returns the exception if an error occurs during execution.

    Notes:
    - Commits changes to the database after execution.
    - Handles any exceptions by returning the exception object, allowing the caller to handle the error.
    """  
    return directOP.insertDataIntoDatabase(sql,params,connection)
   
def insertBatchDataIntoDatabase(sql:str, params:list, connection):    
    """
    Inserts a batch of data into the database using a batched execution.

    :param sql: SQL query string for insertion, typically a parameterized INSERT statement.
    :param params: List of lists, with each inner list representing a set of parameters for one batch entry.
    :param connection: Active database connection object.

    :return: List of tuples with any returned rows from the executed SQL query, or `None` if no rows are returned.
             Returns the exception if an error occurs during execution.

    Notes:
    - Uses `psycopg2.extras.execute_batch` for optimized batch insertion.
    - Commits the transaction after execution and closes the cursor.
    - Handles any exceptions by returning the exception object.
    """
    return directOP.insertBatchDataIntoDatabase(sql,params,connection)

def insertBulkDataIntoDatabase(sql:str, template:str, params:list, connection):  
    """
    Inserts bulk data into the database using a templated value format, optimized for large inserts.

    :param sql: SQL query string for insertion, typically an INSERT statement.
    :param template: Template for each row's values in the bulk insert operation. This is combined with each item in `params` to complete the query.
        - If `params` contains sequences (e.g., lists or tuples), `template` should use positional placeholders (e.g., "(%s, %s, %s)" or "(%s, %s, 42)" for fixed constants).
        - If `params` contains dictionaries, `template` should use named placeholders (e.g., "(%(id)s, %(f1)s, 42)" for fields by name).
    :param params: List of rows to insert, where each row is either a list/tuple (for positional placeholders) or a dictionary (for named placeholders).
                   The structure must match `template`.
    :param connection: Active database connection object for executing the query.

    :return: List of tuples representing rows returned by the query, if any. Returns `None` if no rows are returned.
             If an error occurs during execution, the exception is returned.

    Notes:
    - Uses `psycopg2.extras.execute_values` for efficient bulk insertion, minimizing individual database calls.
    - Commits the transaction after execution and closes the cursor.
    - If an exception is raised during execution, commits the transaction, closes the cursor, and returns the exception.
    """  
    return directOP.insertBulkDataIntoDatabase(sql, template, params, connection)

def insertBulkDataIntoDatabaseByCopyManager(tableAndSchema:str, columns:tuple, params:tuple, connection):  
    """
    Inserts bulk data into a database table using PostgreSQL's CopyManager for high efficiency.

    :param tableAndSchema: Full table name including schema (e.g., "schema.table_name").
    :param columns: Tuple of column names corresponding to the data being inserted.
    :param params: Tuple of data tuples, with each inner tuple representing a row of values.
    :param connection: Active database connection object.

    :return: `None` if successful, or the exception object if an error occurs.

    Notes:
    - Leverages `CopyManager` from `pgcopy` for bulk data insertion, which can be more efficient than traditional insert methods.
    - Commits the transaction after execution and closes the cursor.
    - Handles any exceptions by returning the exception object.
    """  
    return directOP.insertBulkDataIntoDatabaseByCopyManager(tableAndSchema, columns, params, connection)  

def updatetBulkDataInDatabaseByCopyManager(schemaName:str,tableName:str, columns:tuple, params:tuple, updateSql:str, connection):    
    """
    Updates bulk data in a database table using a temporary table and PostgreSQL's CopyManager.

    :param schemaName: Name of the schema where the target table resides.
    :param tableName: Name of the target table to be updated.
    :param columns: Tuple of column names corresponding to the data being inserted/updated.
    :param params: Tuple of data tuples, with each inner tuple representing a row of values for the update.
    :param updateSql: SQL string for the `UPDATE` operation, using the temporary table as a source.
    :param connection: Active database connection object.

    :return: List of tuples with any returned rows from the executed SQL query, or `None` if no rows are returned.
             Returns the exception object if an error occurs.

    Notes:
    - Creates a temporary table to hold bulk data for updating rows in the main table.
    - Uses `CopyManager` to copy bulk data into the temporary table.
    - Executes `updateSql` to update the main table based on the copied data.
    - Commits the transaction after execution and closes the cursor.
    - Returns the exception if an error occurs during execution.
    """
    return directOP.updatetBulkDataInDatabaseByCopyManager(schemaName,tableName, columns, params, updateSql, connection)

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
    return advOP.POST(connection, schema, tableName, data, onConflict, uniqueColumnNamesForConflict)

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
    return advOP.POST_BULK(connection, schema, tableName, data, byCopy, onConflict, uniqueColumnNamesForConflict)

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
    return advOP.PUT(connection, schema, updates, tableName, conditions)

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
    return advOP.PUT_BULK(connection, schema, updates, tableName, conditionColumns)

def SELECT(connection, schema, columns:list, tableName:str, conditions:dict={},default:list=[]):
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
    return advOP.SELECT(connection, schema, columns, tableName, conditions, default)

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
    return advOP.SELECT_FUNCTION(connection, schema,functionName,functionParameter,columns)

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
    return advOP.DELETE(connection, schema, tableName, conditions)

def TRUNCATE(connection, schema, tableName:str):
    """
    Truncates table

    :param connection: Database connection object.
    :param schema: Schema in which the target table resides.
    :param tableName: Name of the table from which rows should be deleted.
    """
    return advOP.TRUNCATE(connection, schema, tableName)