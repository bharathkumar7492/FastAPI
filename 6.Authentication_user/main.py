from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

import models
from database import engine
from routers import user, post



# Create the tables in the database if they do not already exist
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# temp storage
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like biriyani", "id": 2}]
    


# --------
# GET POSTS

@app.get("/")
def root():
    return {"message": "welcome to fastapi"}


app.include_router(user.router)
app.include_router(post.router)