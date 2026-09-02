from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
# Import OAuth2 form to receive username and password from the login form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import database, schemas, models, utils, oauth2



# Create a router for authentication-related endpoints
router = APIRouter(tags=["Authentication"])


# Login endpoint to verify user credentials
@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm=Depends() ,db: Session=Depends(database.get_db)):
    
    """ OAuth2PasswordRequestForm uses the field name username, not email.So even if you send email it takes as username field
    username = user@gmail.com
    password = 123456         --> user_credentials.username     -->     user.email  """
    

    
    # Find the user in the database using the username (email)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If the user does not exist, return 404 error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Compare the entered password with the hashed password from the database
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid Credentials")
    
    # Create a JWT access token containing the user's ID
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

