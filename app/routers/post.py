from .. import models, schemas, utils


# retrieving all post
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return  posts



# Creating the post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):  # refer the Post pydantic model

    new_post = models.Post(**post.dict()) # ** and then to dict opens the dictionary and each column not need to be written
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# Retrieving post with ID
@app.get("/posts/{id}", response_model=schemas.Post)
#def get_post(id : int, response : Response):
def get_post(id : int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    return post




# Deleting the post
@app.delete("/posts/{id}")
def delete_post(id : int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update post
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id : int, post : schemas.PostCreate, db: Session = Depends(get_db)): # Post to send request to right schema

    refresh_post = db.query(models.Post).filter(models.Post.id == id)

    if refresh_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    refresh_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return refresh_post.first()