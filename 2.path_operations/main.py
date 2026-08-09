from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to fastapi"}


@app.get("/posts")
def get_posts():
    return {"data": "this is your posts"}

# Define a POST API endpoint at "/createPosts"
@app.post("/createPosts")
# Function to handle the request and receive the request body
def create_posts(payload: dict = Body(...)):
    # Print the data received from the client
    print(payload)
    # Return the title and content received from the request
    return {"new_post": f"title {payload["title"]} content: {payload["content"]}"}