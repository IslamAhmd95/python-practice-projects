from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    name: str
    email: EmailStr = Field(unique=True)
    password: str


class ShowUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr


class Blog(BaseModel):
    title: str
    body: str
    published: bool = False


class UpdateBlog(BaseModel):
    title: str
    body: str
    published: bool = False


class ShowBlog(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Enable ORM mode, allows Pydantic models to read SQLAlchemy ORM objects because ORM objects are not dictionaries

    title: str
    body: str



class ShowUserWithBlogs(ShowUser):
    blogs: list[ShowBlog] = []


class ShowBlogWithUser(ShowBlog):
    creator: ShowUser


class Login(BaseModel):
    username: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class ShowUserWithToken(ShowUser):
    id: int
    access_token: str
    token_type: str