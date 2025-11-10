from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.auth import router as auth_routers
from src.api.ai import router as ai_routers


@asynccontextmanager  # Special decorator to manage the lifecycle to create an asynchronous context manager
async def lifespan(app: FastAPI):   # means the whole lifespan of my app from start to finish
    print("DB ready.")   # happens at startup
    yield     # app is running here normally (requests)
    print("Shutdown...")  # happens at shutdown



app = FastAPI(
    title="FastAPI Gemini Ai App",
    lifespan=lifespan
)

app.include_router(auth_routers)
app.include_router(ai_routers)