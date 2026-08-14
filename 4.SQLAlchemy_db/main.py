from fastapi import FastAPI
from fastapi.params import Body
# Import randrange to generate a random number
from random import randrange

from schemas import Post



app = FastAPI()

# Store all posts in a list (temp memory)
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
# (to practice path order matter)

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
@app.get("/posts/{id}")
def get_post(id: int): # data validation, that send fro path
    # Find the post using the given ID
    post = find_post(id)
    print(post)
    return {"post_detail": post}






# CREATE POSTS

# Create a new post
@app.post("/createPosts")
def create_posts(new_post: Post):
    # Convert the Pydantic object into a dictionary
    post_dict = new_post.dict()
    # Generate a random ID for the new post
    post_dict["id"] = randrange(0, 1000)

    # Add the new post to the list
    my_posts.append(post_dict)
    # Return the newly created post
    return {"data": post_dict}