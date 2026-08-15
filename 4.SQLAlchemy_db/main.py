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




# DELETE POSTS

# Find the index of a post using its ID
def find_index_post(id):
    # Go through the list with index and post  
    for index, post in enumerate(my_posts):
        # Check if the post ID matches & return that post index
        if post["id"] == id:
            return index

# Delete a post using its ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Find the index of the post with the given ID
    index = find_index_post(id)
    
    # If post does not exist -  Return 404 Not Found error
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # Remove the post from the list
    my_posts.pop(index)
    # Return 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
# UPDATE POST

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # Find the index of the post with the given ID
    index = find_index_post(id)   

    # If post does not exist -  Return 404 Not Found error
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist" )
        
    # Convert the Pydantic 'post' object into a normal Python dictionary
    post_dict = post.dict()    
    
    # Add the ID from the URL to the new post data
    # Example: PUT /posts/1 → id = 1
    post_dict["id"] = id         
   # why put id: because the request body contains only the new post data, usually without the ID.
            
    # Replace the old post with the new post at the same index
    my_posts[index] = post_dict
            
    # Return the updated post as the response
    return {"data": post_dict}
