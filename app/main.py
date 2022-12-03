from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# creating the model
# define class and extend BaseModel, to control and validate the data posted
class Post(BaseModel): # pydantic model
    title : str
    content : str
    published : bool = True
    #rating : Optional[int] = None

# array to save posts in memory temporarily
my_posts = [{"title" : "title 1", "content" : "content 1", "id" : 1}, 
{"title" : "title 2", "content" : "content 2", "id" : 2}, 
{"title" : "title 3", "content" : "content 3", "id" : 3}]

#finding post with ID
def find_post(id):
    #print(type(id))
    for p in my_posts:
        if p["id"] == id:
            return p


"""#path operation/route
@app.get("/") # decorator to give endpoint in API, consists of @ appname and then http method with path for user
def root():  # function, if async for asynchronous task
    return {"message" : "Welcome to my api!!!!!!"}"""

# retrieving all post
@app.get("/posts")
def get_posts():
    return  {"Data" : my_posts}

# Creating the post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):  # refer the Post pydantic model
    print(post)
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

# Retrieving post with ID
@app.get("/posts/{id}")
#def get_post(id : int, response : Response):
def get_post(id : int):
    #print(type(id))
    #ID = int(id)
    post = find_post(id)
    if not post:
        # done mannually, can raise a http exception
        #response.status_code = status.HTTP_404_NOT_FOUND  
        #return{'message' : f"post with id : {id} not found"}
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