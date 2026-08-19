# Import PyMySQL to connect Python with MySQL database
import pymysql
# Import DictCursor to get database results as dictionaries
from pymysql.cursors import DictCursor
# Import time to add a delay before trying to connect again
import time


# Keep trying until the database connection is successful
while True:

    try:
        # Connect Python to the MySQL database
        connection = pymysql.connect(
            host="localhost",          # MySQL is running on this computer
            database="fastapi_db",     # Database name
            user="root",               # MySQL username
            password="bharath",        # MySQL password

            # Return query results in dictionary format
            # Example: {"id": 1, "title": "Hello"}
            cursorclass=DictCursor
        )
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        # Display a success message
        print("Database connection was successful")
        # Stop the while loop because connection succeeded
        break

    except Exception as error:
        # Display message if database connection fails
        print("Connecting to database failed")
        # Display the actual error
        print("Error:", error)
        # Wait 2 seconds before trying to connect again
        time.sleep(2)