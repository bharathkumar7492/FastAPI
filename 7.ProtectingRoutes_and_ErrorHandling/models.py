# sqlalchemy models = What tables look like & Works with the database


# Import Base so this class can become a SQLAlchemy database model
from database import Base
# Import SQLAlchemy column types
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


# Create a Post database model
class Post(Base):

    # Specify the database table name
    __tablename__ = "posts"

    # Create the ID, title, content & published columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, server_default=text("TRUE"), nullable=False)
    
    # Store the date and time when the post is created
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    
   
   
# Create a User database model
class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))