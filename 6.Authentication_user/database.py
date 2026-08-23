import pymysql
from pymysql.cursors import DictCursor
import time



# Import create_engine to create a connection between SQLAlchemy and the database
from sqlalchemy import create_engine
# Import sessionmaker to create database sessions
from sqlalchemy.orm import sessionmaker
# Import declarative_base to create the base class for database models
from sqlalchemy.ext.declarative import declarative_base



# Database connection URL
# Format: dialect+driver://username:password@host/database
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:bharath@localhost/fastapi_db"


# Create the SQLAlchemy engine to communicate with MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Create a session factory to interact with the database
SessionLocal = sessionmaker(
                            autocommit=False,      # changes are not automatically saved
                            autoflush=False,       # changes are not automatically sent to the database
                            bind=engine            # connect this session to our database engine
                            )

# Create a base class that will be used to create database models
Base = declarative_base()
# Base is the parent class for all database models.It's what connects your Python classes to actual database tables.
# Any class that inherits from Base is treated by SQLAlchemy as a database table.
# Without Base, SQLAlchemy would treat the class as a normal Python class.


# Dependency
# Create a database session for each request
def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Give the database session to the API endpoint
        yield db
    finally:
        # Close the database session after the request is finished
        db.close()








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