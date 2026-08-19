from fastapi import FastAPI, Response, status, HTTPException
# FastAPI - create the API, Response - control the HTTP response
# status - use HTTP status codes, HTTPException - return API errors
from fastapi.params import Body
from random import randrange

from schemas import Post
from database import cursor, connection



app = FastAPI()

# temp storage
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like biriyani", "id": 2}]


# GET POSTS

@app.get("/")
def root():
    return {"message": "welcome to fastapi"}


# GET endpoint to fetch all posts from the database
@app.get("/posts")
def get_posts():
    
    # Execute SQL query to get all posts from the posts table
    cursor.execute("""SELECT * FROM posts""")
    # Get all rows returned by the SQL query
    posts = cursor.fetchall()
    # Return all posts as the API response
    return {"data": posts}



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
    
    # Find the post in the database using query with given ID
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # Get the matching post returned by the SQL query
    post = cursor.fetchone()
    print(post)
    if not post:
        # Stop the function and return 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail= "post with id: {id} was not found")
    return {"post-detail": post}




# CREATE POSTS

# Create a new post
@app.post("/createPosts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    # Insert the post data into the posts table
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """,
                   # Pass the values safely to the SQL query
                  (post.title, post.content, post.published))
    
    # Get the newly created post
    new_post = cursor.fetchone()
    # Save the changes permanently in the database
    connection.commit()
    # Return the created post to the client
    return {"data": new_post}




# DELETE POSTS

# Find the index of a post using its ID
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

# Delete a post using its ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    # Delete the post from the database using query with given ID
    cursor.execute(""" DELETE FROM posts WHERE id = %s """, (str(id),))
    # Get the deleted post
    deleted_post = cursor.fetchone()
    # Save the delete operation permanently in the database
    connection.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # Return 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
    
# UPDATE POST

# PUT endpoint to update an existing post using its ID
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    # Update the post using query  WHERE id = %s ensures only the post with the given ID is updated
    cursor.execute("""
                   UPDATE posts
                   SET title = %s, content = %s, published = %s
                   WHERE id = %s""",
                   (post.title, post.content, post.published, str(id)))
    # Get the updated post
    updated_post = cursor.fetchone()
    # Save the update permanently in the database
    connection.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist" )
        
    return {"data": updated_post}