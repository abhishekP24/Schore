import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",          # Localhost for local MySQL
            user="root",          # Your MySQL username
            password="Mysql@123",  # Your MySQL password
            database="school_project"    # Your database name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None