from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from app.database import engine, Base
from app.routers.blogs import router as blog_router
from app.routers.users import router as user_router
from app.routers.auth import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(blog_router)







"""
Notes:
    - `db: Session` tells FastAPI & IDE that db is a SQLAlchemy Session object)
    - `Depends(get_db)` tells FastAPI to use the get_db dependency to provide a database session for this endpoint.
"""