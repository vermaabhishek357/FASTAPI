from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


# define class and extend BaseModel, to control and validate the data posted
class Post(BaseModel): # pydantic model
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

# array to save posts in memory temporarily
my_posts = [{"title" : "title 1", "content" : "content 1", "id" : 1}, {"title" : "title 2", "content" : "content 2", "id" : 2}]

def find_post(id):
    #print(type(id))
    for p in my_posts:
        if p["id"] == id:
            return p


"""#path operation/route
@app.get("/") # decorator to give endpoint in API, consists of @ appname and then http method with path for user
def root():  # function, if async for asynchronous task
    return {"message" : "Welcome to my api!!!!!!"}"""

@app.get("/posts")
def get_posts():
    return  {"Data" : my_posts}


@app.post("/posts")
def create_posts(post : Post):  # refer the Post pydantic model
    print(post)
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/{id}")
def get_post(id : int):
    #print(type(id))
    #ID = int(id)
    post = find_post(id)
    return {"post_detail" : post}

# title str, content str, 