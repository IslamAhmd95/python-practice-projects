from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from app.api import auth
from app.api import users


app = FastAPI(
    title="Blog API",
    description="A simple blog API built with FastAPI + SQLAlchemy",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(users.router)