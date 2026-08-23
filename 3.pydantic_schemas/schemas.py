# pydantic schemas/models = Validates request data

# Import BaseModel from Pydantic to create data validation schemas
from pydantic import BaseModel
# Import Optional to make a field optional
from typing import Optional


# Create a Pydantic model/schema for a Post
class Post(BaseModel):
    title: str              #  Title is required and must be a string
    content: str            # Content is required and must be a string
    published: bool=True    # Published is optional; if not provided, its default value is True
    rating: Optional[int]=None  # Rating is optional; it can be an integer or None