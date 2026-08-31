# Import CryptContext to handle password hashing
from passlib.context import CryptContext


# Create a password hashing tool using bcrypt
password_context = CryptContext(schemes=["bcrypt"],  # Use bcrypt to hash passwords
                           deprecated="auto")   # Automatically handle old hashing schemes


def hash(password: str):
    return password_context.hash(password)