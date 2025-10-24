import os
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with sessionLocal() as db:
        yield db


class BaseModel(DeclarativeBase):
    __abstract__ = True
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped["DateTime"] = mapped_column(  
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped["DateTime"] = mapped_column(   
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
