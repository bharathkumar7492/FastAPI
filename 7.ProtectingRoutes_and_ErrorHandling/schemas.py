# Import BaseModel from Pydantic to create data validation schemas
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Create a Pydantic model/schema for a Post
class PostBase(BaseModel):
    title: str             
    content: str            
    published: bool = True    


# Schema used when creating a new post
class CreatePost(PostBase):
    pass


# Schema used for the API response
class PostResponse(PostBase):
    # title, content, published columns will be inherits from PostBase class
    id: int
    created_at: datetime
    
    # Allow Pydantic to read data from SQLAlchemy model
    class config:
        orm_mode = True
        
        
        

# USERS SCHEMAS  ----------------------

#  schema used for create user
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    

# schema used for user response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    # Allow Pydantic to read data from SQLAlchemy model
    class config:
        orm_mode = True
        

# Schema for validating user login credentials
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    


# Schema for the login response
class Token(BaseModel):
    access_token: str
    token_type: str         # Type of token (usually "bearer")

    

# Schema for storing data extracted from the JWT
class TokenData(BaseModel):
    id: Optional[int] = None