# Import JWT tools for creating and handling JSON Web Tokens
from jose import JWTError, jwt
# Import datetime tools to set the JWT expiration time
from datetime import datetime, timedelta


# Secret key used to sign and verify the JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# Algorithm used to sign the JWT
ALGORITHM = "HS256"
# JWT will expire after 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Create a JWT access token
def create_access_token(data: dict):
    # Copy the user data that will be stored inside the token
    to_encode = data.copy()
    
    # Calculate the token expiration time
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add expiration time to the token data
    to_encode.update({"exp": expire})
    
    # Create and sign the JWT using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Return the generated JWT
    return encoded_jwt

