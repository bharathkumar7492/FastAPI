from fastapi import FastAPI, Response, status, HTTPException
# FastAPI - create the API, Response - control the HTTP response
# status - use HTTP status codes, HTTPException - return API errors
from fastapi.params import Body
from random import randrange

from schemas import Post



app = FastAPI()

# temp storage
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like biriyani", "id": 2}]


# GET POSTS

@app.get("/")
def root():
    return {"message": "welcome to fastapi"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# GET LATEST POST 

#  Get the latest post from the list
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post



# GET SPECIFIC POST

# Find a post using its ID
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

# Get a specific post using its ID

# Set the response status code manually
@app.get("/posts/{id}")
def get_post(id: int, response: Response): 
    post = find_post(id)
    # if the post is not found
    if not post:
        # Set status code to 404 (Not Found)
        response.status_code = status.HTTP_404_NOT_FOUND
        # Return error message
        return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}

# or 

# Use HTTPException to return an error response (BETTER to use)
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        # Stop the function and return 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail= "post with id: {id} was not found")
    return {"post-detail": post}



# CREATE POSTS

# Create a new post
@app.post("/createPosts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 1000)
    my_posts.append(post_dict)
    return {"data": post_dict}