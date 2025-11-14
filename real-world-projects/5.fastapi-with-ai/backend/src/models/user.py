from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    username: str = Field(unique=True, max_length=100)
    email: EmailStr = Field(unique=True, max_length=255) 
    password: str = Field(min_length=8, max_length=255)