# Import APIRouter to create a group of related API routes
from fastapi import APIRouter
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# Import Session to work with the SQLAlchemy database session
from sqlalchemy.orm import Session 

import models, schemas, utils
from database import get_db


# Create a router with a common URL prefix and group name in Swagger docs
router = APIRouter(
    prefix= "/users",   # Adds '/users' to all routes in this router
    tags= ["Users"]     # Groups these routes under "Users" in /docs
)

# we prefix the path here, so in every path "/users" is automatically added no need to mention


# CREATE USER

# Create a new user and return the created user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session=Depends(get_db)):
    
    # Hash the user's plain password before storing it in the database
    user.password  = utils.hash(user.password)
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



# GET USER

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:  {id} does not exist")
    
    return user