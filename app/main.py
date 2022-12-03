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

# find  the index in array with the id
def find_index_post(id : int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Deleting the post
@app.delete("/posts/{id}")
def delete_post(id : int, status_code=status.HTTP_204_NO_CONTENT):

    # find  the index in array with the id
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post
@app.put("/posts/{id}")
def update_post(id : int, post : Post): # Post to send request to right schema

    print(post)
    # find  the index in array with the id
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id} does not exist")
    
    post_dict = post.dict() # convert json post to dictionary
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}
# title str, content str, 