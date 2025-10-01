import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

engine = create_engine(DATABASE_URL, echo=False)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class BaseModel(DeclarativeBase):
    __abstract__ = True
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
