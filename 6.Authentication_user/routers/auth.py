from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

import database, schemas, models, utils, oauth2



# Create a router for authentication-related endpoints
router = APIRouter(tags=["Authentication"])


# Login endpoint to verify user credentials
@router.post("/login")
def login(user_credentials: schemas.UserLogin ,db: Session=Depends(database.get_db)):
    # Find the user in the database using the email
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    # If the user does not exist, return 404 error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    # Compare the entered password with the hashed password from the database
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid Credentials")
    
    # create token
    # return token
    
    # Create a JWT access token containing the user's ID
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

