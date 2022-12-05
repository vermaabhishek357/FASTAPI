from fastapi import status, HTTPException, Depends
from .. import models, schemas, utils
from ..database import engine, get_db
from sqlalchemy.orm import Session
from ..main import app

@app.post("/users", status_code=status.HTTP_201_CREATED,  response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password frim user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) # ** and then to dict opens the dictionary and each column not need to be written
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", status_code=status.HTTP_201_CREATED,  response_model=schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return user