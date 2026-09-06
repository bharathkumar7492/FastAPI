from fastapi import FastAPI

import models
from database import engine
from routers import user, post, auth



# Create the tables in the database if they do not already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to fastapi"}


# Register the user, post, and authentication routers with the main FastAPI app
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)