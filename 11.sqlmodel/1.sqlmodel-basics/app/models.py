from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=120)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
