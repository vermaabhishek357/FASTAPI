from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()


# define class and extend BaseModel, to control and validate the data posted
class 

#path operation/route
@app.get("/") # decorator to give endpoint in API, consists of @ appname and then http method with path for user
def root():  # function, if async for asynchronous task
    return {"message" : "Welcome to my api!!!!!!"}

@app.get("/posts")
def get_posts():
    return  {"Data" : "This is your post"}


@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post" :  f"title : {payLoad['Title']} content : {payLoad['Content']}"}

# title str, content str, 