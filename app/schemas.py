from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# creating the model
# define class and extend BaseModel, to control and validate the data posted

class PostBase(BaseModel): # pydantic model
    title : str
    content : str
    published : bool = True
    #rating : Optional[int] = None

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
   email : EmailStr
   password: str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
     id : Optional[str] = None


class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)

    class Config:
        orm_mode = True