from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
# Import CryptContext to handle password hashing
from passlib.context import CryptContext

from schemas import PostBase, CreatePost, PostResponse, CreateUser, UserResponse
from database import cursor, connection

import models
from database import engine, get_db
# Import Session to work with the SQLAlchemy database session
from sqlalchemy.orm import Session 





# Create a password hashing tool using bcrypt
password_context = CryptContext(schemes=["bcrypt"],  # Use bcrypt to hash passwords
                           deprecated="auto")   # Automatically handle old hashing schemes

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


# GET endpoint to fetch all posts from the database
# If want to return multiple posts use -'list[]' in response_model
@app.get("/posts", response_model=list[PostResponse])
              # FastAPI gets a database session from get_db()
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()


    # Query the Post table and get all posts
    posts = db.query(models.Post).all()
    # Return all posts as the API response
    return posts



# GET SPECIFIC POST

# Get a specific post using its ID
@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    
    # Find the post with the given ID in the database
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        # Stop the function and return 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail= "post with id: {id} was not found")
    return post




# CREATE POSTS

# Create a new post
@app.post("/createPosts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: CreatePost, db: Session=Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """,
    #               (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    
    
    
    # # Create a SQLAlchemy Post object using the received data
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # If the model has many fields(columns), use unpacking to avoid writing each field manually
    # Convert Pydantic model to dictionary 
    new_post = models.Post(**post.dict())
    
    # Add the new post to the database session
    db.add(new_post)
    # Save the new post permanently in the database
    db.commit()
    # Get the newly created post data from the database
    db.refresh(new_post)
    
    
    # Return the created post to the client
    return new_post




# DELETE POSTS

# Delete a post using its ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s """, (str(id),))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    
    
    
    #  Find the post with the given ID
    post = db.query(models.Post).filter(models.Post.id == id)
    
    # Check if the post exists, if not return 404 error message
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    # Delete the matching post from the database
    post.delete(synchronize_session=False)
    
    # Save the delete operation permanently in the database
    db.commit()
    
    # Return 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
    
# UPDATE POST

# PUT endpoint to update an existing post using its ID
@app.put("/posts/{id}", response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session=Depends(get_db)):
    # cursor.execute("""
    #                UPDATE posts
    #                SET title = %s, content = %s, published = %s
    #                WHERE id = %s""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    
    
    
    
    # Find the post with the given ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # Get the first matching post
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist" )
    
    # Update the post using the data received from the client
    post_query.update(updated_post.dict(), synchronize_session=False)
    # Save the changes permanently in the database
    db.commit()
        
    return post_query.first()





# --------------
# CREATE USER


# Create a new user and return the created user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, db: Session=Depends(get_db)):
    
    # Hash the user's plain password before storing it in the database
    user.password  = password_context.hash(user.password)
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user