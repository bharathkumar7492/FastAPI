# Import APIRouter to create a group of related API routes
from fastapi import APIRouter
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# Import Session to work with the SQLAlchemy database session
from sqlalchemy.orm import Session 

import models, schemas, oauth2
from database import get_db



# Create a router with a common URL prefix and group name in Swagger docs
router = APIRouter(
    prefix="/posts",   # Adds /posts to all routes in this router
    tags=["Posts"]     # Groups these routes under "Posts" in /docs
)


# GET ALL

@router.get("/", response_model=list[schemas.PostResponse])
              # FastAPI gets a database session from get_db()
def get_posts(db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()


    # Query the Post table and get all posts
    posts = db.query(models.Post).all()
    
    '''for gets only users own posts'''
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    
    # Return all posts as the API response
    return posts



# GET SPECIFIC POST

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    
    # Find the post with the given ID in the database
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        # Stop the function and return 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail= "post with id: {id} was not found")
        
    
    '''for gets only users own posts'''
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")    
        
    
    return post




# CREATE POSTS

# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """,
    #               (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    
    
    
    print(current_user.id)
    
    # Create a new post and assign it to the current user by Get the ID of the currently logged-in user
    new_post = models.Post(user_id=current_user.id, **post.dict())
    
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s """, (str(id),))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    
    
    #  Find the post with the given ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # Get the actual post object
    post = post_query.first()
    
    # Check if the post exists, if not return 404 error message
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # Check if the current user owns the post
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    # Delete the matching post from the database
    post_query.delete(synchronize_session=False)
    
    # Save the delete operation permanently in the database
    db.commit()
    
    # Return 204 No Content response
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
    
# UPDATE POST

# PUT endpoint to update an existing post using its ID
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
        
        
    # Check if the current user owns the post
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
        
    
    # Update the post using the data received from the client
    post_query.update(updated_post.dict(), synchronize_session=False)
    # Save the changes permanently in the database
    db.commit()
        
    return post_query.first()


