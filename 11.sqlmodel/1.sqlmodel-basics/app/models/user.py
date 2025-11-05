from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    name: str = Field(max_length=100)
    secret_name: str | None = Field(default=None, max_length=100)
    email: EmailStr = Field(max_length=120)
    age: int | None = Field(default=None, ge=18)

class User(UserBase, table=True):  # classes with table=True go to the DB.
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)

