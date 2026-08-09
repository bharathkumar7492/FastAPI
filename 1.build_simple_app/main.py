
# Import the FastAPI class from the fastapi package
from fastapi import FastAPI

# Create a FastAPI application instance
app = FastAPI()

# Define a GET API endpoint at "/"
@app.get("/")
# Function that runs when the "/" endpoint is requested
def root():
    return {"message": "welcome to fastapi"}