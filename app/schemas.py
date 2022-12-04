from pydantic import BaseModel
from datetime import datetime


# creating the model
# define class and extend BaseModel, to control and validate the data posted

class PostBase(BaseModel): # pydantic model
    title : str
    content : str
    published : bool = True
    #rating : Optional[int] = None

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id : int
    created_at : datetime

    class Config:
        orm_mode = True

        