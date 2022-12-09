from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

print(settings.database_username)

#call create engine to create tables from models using sqlalchemy
#models.Base.metadata.create_all(bind=engine) # commented as alembic is being used to migrate to database

# initiate the app
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)