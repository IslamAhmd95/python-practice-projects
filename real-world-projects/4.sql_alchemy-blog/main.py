from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from app.api import auth
from app.api import users
from app.api import tags
from app.api import posts
from app.api import comments


app = FastAPI(
    title="FastAPI Blog",
    description="A simple blog API built with FastAPI + SQLAlchemy",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tags.router)
app.include_router(posts.router)
app.include_router(comments.router)