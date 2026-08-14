# Import BaseModel from Pydantic to create data validation schemas
from pydantic import BaseModel
from typing import Optional


# Create a Pydantic model/schema for a Post
class Post(BaseModel):
    title: str             
    content: str            
    published: bool=True    
    rating: Optional[int]=None  