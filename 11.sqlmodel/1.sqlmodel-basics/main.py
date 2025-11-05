from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.users import router as users_routers

@asynccontextmanager  # Special decorator to manage the lifecycle to create an asynchronous context manager
async def lifespan(app: FastAPI):   # means the whole lifespan of my app from start to finish
    # SQLModel.metadata.create_all(engine)   # Before API starts (creates tables) , removed if using alembic
    print("DB ready.")   # happens at startup
    yield     # app is running here normally (requests)
    print("Shutdown...")  # happens at shutdown

app = FastAPI(lifespan=lifespan)

app.include_router(users_routers)
