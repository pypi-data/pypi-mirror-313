import psycopg2
from pgcopy import CopyManager

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
    cursor = connection.cursor()
    try:
        cursor.execute(sql,params)
        result = cursor.fetchall()
        return result
    except Exception as e:
        return e

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
    cursor = connection.cursor()
    try:
        cursor.execute(sql,params)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        if len(result) > 0:
            return result
        return None
    except Exception as e:
        connection.commit()
        cursor.close()
        return e

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
    cursor = connection.cursor()
    try:
        psycopg2.extras.execute_batch(cursor, sql, params)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        if len(result) > 0:
            return result
        return None
    except Exception as e:
        connection.commit()
        cursor.close()
        return e

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
    cursor = connection.cursor()
    try:
        psycopg2.extras.execute_values(cursor, sql, params, template)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        if len(result) > 0:
            return result
        return None
    except Exception as e:
        connection.commit()
        cursor.close()
        return e


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
    cursor = connection.cursor()
    try:
        mgr = CopyManager(connection, tableAndSchema, columns)
        mgr.copy(params)
        
        connection.commit()
        cursor.close()
        return None
    except Exception as e:
        connection.commit()
        cursor.close()
        return e

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
    cursor = connection.cursor()
    table = schemaName + '.' + tableName
    temp = schemaName + '_tmp_' + tableName
    try:
        #cursor.execute(f"""CREATE TEMP TABLE {temp} ON COMMIT DROP AS SELECT * FROM {table} LIMIT 0;""")
        cursor.execute(f"""CREATE TEMP TABLE {temp} (LIKE {table} INCLUDING DEFAULTS) ON COMMIT DROP;""")
        mgr = CopyManager(connection, temp, columns)
        mgr.copy(params)
        cursor.execute(updateSql)
        result = cursor.fetchall()

        connection.commit()
        cursor.close()
        if len(result) > 0:
            return result
        return None
    except Exception as e:
        connection.commit()
        cursor.close()
        return e