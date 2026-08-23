# Import BaseModel from Pydantic to create data validation schemas
from pydantic import BaseModel
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
        
        
        