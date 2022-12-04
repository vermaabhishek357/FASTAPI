from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

#call create engine to create tables from models
models.Base.metadata.create_all(bind=engine)


# initiate the app
app = FastAPI()

# connect pyscopg2 to postgresql fastapi database
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'Qazwsx123#', 
        cursor_factory = RealDictCursor) # pass host, database, user, password in connect method
        cursor = conn.cursor()
        print("Connection to database successfully created")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error : ", error)
        time.sleep(1)


# retrieving all post
@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    #run sql query and call it, using SQL query and ORM
    #cursor.execute("""SELECT * FROM posts""")  # sql query to get alll data
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    return  posts



# Creating the post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):  # refer the Post pydantic model

    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #            (post.title, post.content, post.published))
    #new_post = cursor.fetchone() # fetch the posted data

    #conn.commit() # Commit the changes made to database table

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict()) # ** and then to dict opens the dictionary and each column not need to be written
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# Retrieving post with ID
@app.get("/posts/{id}", response_model=schemas.Post)
#def get_post(id : int, response : Response):
def get_post(id : int, db: Session = Depends(get_db)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))  # sql query to get alll data
    #post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    return {"post_detail" : post}




# Deleting the post
@app.delete("/posts/{id}")
def delete_post(id : int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):

    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))  # sql query to get alll data
    #post = cursor.fetchone()
    #conn.commit() # Commit the changes made to database table

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update post
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id : int, post : schemas.PostCreate, db: Session = Depends(get_db)): # Post to send request to right schema

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #            (post.title, post.content, post.published, str(id),))  # sql query to get alll data
    #post = cursor.fetchone()
    #conn.commit() # Commit the changes made to database table

    refresh_post = db.query(models.Post).filter(models.Post.id == id)

    if refresh_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    refresh_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return refresh_post.first()
