from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

#call create engine to create tables from models
models.Base.metadata.create_all(bind=engine)

# initiate the app
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)