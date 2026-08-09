from fastapi import FastAPI

from schemas import Post



app = FastAPI()



@app.get("/")
def root():
    return {"message": "welcome to fastapi"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your posts"}


# practice
# Create a POST API endpoint at "/createPosts"
#  @app.post("/createPosts")
# def create_posts(new_post: Post):
#     # extract data from post
#     print(new_post.title)
#     print(new_post.published)
#     print(new_post.rating)
#     return {"data": "new post"}


# Create a POST API endpoint at "/createPosts"
@app.post("/createPosts")
# Receive and validate the request body using the Post schema
def create_posts(new_post: Post):
    # extract data from post
    # print(new_post.title)
    
    # Print the complete Pydantic Post object
    print(new_post)
    
    # Convert the Pydantic object into a Python dictionary
    print(new_post.dict())
    
    # Return the received Post data as the API response
    return {"data": new_post}