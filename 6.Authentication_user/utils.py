# Import CryptContext to handle password hashing
from passlib.context import CryptContext


# Create a password hashing tool using bcrypt
password_context = CryptContext(schemes=["bcrypt"],  # Use bcrypt to hash passwords
                           deprecated="auto")   # Automatically handle old hashing schemes


# Hash the plain password before storing it in the database
def hash(password: str):
    return password_context.hash(password)


# Verify the entered password against the stored hashed password
def verify(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)
