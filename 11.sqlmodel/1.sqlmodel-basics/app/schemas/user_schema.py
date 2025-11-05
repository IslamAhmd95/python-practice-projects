from pydantic import BaseModel, EmailStr, ConfigDict, Field



class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserCreate(UserBase):
    name: str = Field(max_length=100)
    secret_name: str | None = Field(default=None, max_length=100)
    age: int = Field(ge=18)


class UserUpdate(UserBase):
    name: str | None = Field(default=None, max_length=100)
    secret_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18)