from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# define class and extend BaseModel, to control and validate the data posted
class Post(BaseModel): # pydantic model
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

#path operation/route
@app.get("/") # decorator to give endpoint in API, consists of @ appname and then http method with path for user
def root():  # function, if async for asynchronous task
    return {"message" : "Welcome to my api!!!!!!"}

@app.get("/posts")
def get_posts():
    return  {"Data" : "This is your post"}


@app.post("/createposts")
def create_posts(post : Post):  # refer the Post pydantic model
    print(post)
    return {"data" : post}

# title str, content str, 