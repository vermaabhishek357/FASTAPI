from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List
#from ..main import app


router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

# retrieving all post
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()

    return  posts



# Creating the post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):  # refer the Post pydantic model

    print(user_id)
    new_post = models.Post(**post.dict()) # ** and then to dict opens the dictionary and each column not need to be written
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Retrieving post with ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    return post




# Deleting the post
@router.delete("/{id}")
def delete_post(id : int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT, user_id : int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, post : schemas.PostCreate, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)): # Post to send request to right schema

    refresh_post = db.query(models.Post).filter(models.Post.id == id)

    if refresh_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    refresh_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return refresh_post.first()