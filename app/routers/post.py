from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from .. import models, schemas, utils, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session

#from ..main import app


router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

# retrieving all post
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 25, skip : int = 0, search : Optional[str] = ""):
    
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # to get post for logged in user
    #posts = db.query(models.Post).all()


    return  posts



# Creating the post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):  # refer the Post pydantic model

    #print(current_user.email)
    new_post = models.Post(owner_id  = current_user.id, **post.dict()) # ** and then to dict opens the dictionary and each column not need to be written
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Retrieving post with ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db), current_user  : int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
        # query if post belong to same user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    
    return post




# Deleting the post
@router.delete("/{id}")
def delete_post(id : int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT, current_user  : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    # query if post belong to same user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, post_update : schemas.PostCreate, db: Session = Depends(get_db), current_user  : int = Depends(oauth2.get_current_user)): # Post to send request to right schema

    refresh_post = db.query(models.Post).filter(models.Post.id == id)

    post = refresh_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    # query if post belong to same user
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    refresh_post.update(post_update.dict(), synchronize_session=False)
    db.commit()

    return refresh_post.first()