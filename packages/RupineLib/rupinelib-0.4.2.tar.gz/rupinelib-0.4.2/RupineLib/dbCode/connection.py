import psycopg2

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
    connectionStr = "postgres://{}:{}@{}:{}/{}".format(user,pw,host,Port,database)
    connection =  psycopg2.connect(connectionStr, sslmode='require')
    return connection

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
    connection =  psycopg2.connect(connectionStr, sslmode='require')
    return connection
