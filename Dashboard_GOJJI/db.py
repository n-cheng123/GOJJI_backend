import mysql.connector

db_config = {
    'host': 'gator4236.hostgator.com',
    'user': 'sevenlog_gojji',
    'password': 'Test1234',
    'database': 'sevenlog_gojjidw',
    'port': 3306
}

def get_connection():
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        return connection
    else:
        raise ConnectionError("Failed to connect to the database.")