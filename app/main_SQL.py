from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# initiate the app
app = FastAPI()

# creating the model
# define class and extend BaseModel, to control and validate the data posted
class Post(BaseModel): # pydantic model
    title : str
    content : str
    published : bool = True
    #rating : Optional[int] = None


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


"""#path operation/route
@app.get("/") # decorator to give endpoint in API, consists of @ appname and then http method with path for user
def root():  # function, if async for asynchronous task
    return {"message" : "Welcome to my api!!!!!!"}"""

# retrieving all post
@app.get("/posts")
def get_posts():

    cursor.execute("""SELECT * FROM posts""")  # sql query to get alll data
    posts = cursor.fetchall()

    return  {"Data" : posts}



# Creating the post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):  # refer the Post pydantic model

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                (post.title, post.content, post.published))
    new_post = cursor.fetchone() # fetch the posted data

    conn.commit() # Commit the changes made to database table

    return {"data" : new_post}



# Retrieving post with ID
@app.get("/posts/{id}")
#def get_post(id : int, response : Response):
def get_post(id : int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))  # sql query to get alll data
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    
    return {"post_detail" : post}




# Deleting the post
@app.delete("/posts/{id}")
def delete_post(id : int, status_code=status.HTTP_204_NO_CONTENT):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))  # sql query to get alll data
    post = cursor.fetchone()
    conn.commit() # Commit the changes made to database table

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update post
@app.put("/posts/{id}")
def update_post(id : int, post : Post): # Post to send request to right schema

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                (post.title, post.content, post.published, str(id),))  # sql query to get alll data
    post = cursor.fetchone()
    conn.commit() # Commit the changes made to database table

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    

    return {"data" : post}
# title str, content str, 