# Import JWT tools for creating and handling JSON Web Tokens
from jose import JWTError, jwt
# Import datetime tools to set the JWT expiration time
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
# Import OAuth2 authentication scheme
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import schemas, database, models


# Tell FastAPI where the login endpoint is
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



# Secret key used to sign and verify the JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Algorithm used to sign the JWT
ALGORITHM = "HS256"
# JWT will expire after 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Create a JWT access token
def create_access_token(data: dict):
    # Copy the user data that will be stored inside the token
    to_encode = data.copy()
    
    # Calculate the token expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add expiration time to the token data
    to_encode.update({"exp": expire})
    
    # Create and sign the JWT using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Return the generated JWT
    return encoded_jwt



# Verify the JWT token and get the user's ID from it
def verify_access_token(token: str, credential_exception):

    try:
        # Decode the token and verify its signature and validity
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Get the user ID stored inside the token
        id: str = payload.get("user_id")

        # If user ID is missing, raise authentication error
        if id is None:
            raise credential_exception

        # Store the user ID in the TokenData schema
        token_data = schemas.TokenData(id=id)

    # If the token is invalid or expired, raise authentication error
    except JWTError:
        raise credential_exception

    # Return the validated token data
    return token_data


# Get and verify the current user's JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    
    # Error to return when the token is invalid
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    # Verify the token and return the user information
    token = verify_access_token(token, credentials_exception)
    
    # Find the user in the database using the ID from the token
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    # Return the current user's database information
    return user