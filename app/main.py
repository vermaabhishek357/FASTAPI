from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

print(settings.database_username)

#call create engine to create tables from models
models.Base.metadata.create_all(bind=engine)

# initiate the app
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)