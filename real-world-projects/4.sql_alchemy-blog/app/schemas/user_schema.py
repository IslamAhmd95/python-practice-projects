from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.schemas.post_schema import ReadTagSchema
from app.core.enums import OrderEnum
from typing import List


class ResponseBase(BaseModel):
    message: str | None = None
    success: bool = True


class UserFilter(BaseModel):
    offset: int = 0
    limit: int = 10
    order: OrderEnum = OrderEnum.ASC


class ReadUserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bio: str | None = None


class UserPostsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    tags: List[ReadTagSchema] = Field(default_factory=list)


class ReadUserPostsSchema(BaseModel):
    posts: List[UserPostsSchema] = Field(default_factory=list)
    total: int
    page: int
    limit: int


class ReadUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    email: EmailStr
    profile: ReadUserProfile


class ReadAllUsersSchema(BaseModel):
    users: List[ReadUser] = Field(default_factory=list)
    total: int
    page: int
    limit: int

    
class AfterDeleteUser(ResponseBase):
    pass


class UpdateMe(BaseModel):
    name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    bio: str | None = None


class AfterUpdateMe(ResponseBase):
    model_config = ConfigDict(from_attributes=True)

    user: ReadUser


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


class AfterUpdatePassword(ResponseBase):
    pass


class AfterFollowUser(ResponseBase):
    pass


class AfterUnfollowUser(ResponseBase):
    pass


class ReadUserBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str | None = None


class ReadFollowers(BaseModel):
    followers: list[ReadUserBrief]


class ReadFollowing(BaseModel):
    following: list[ReadUserBrief]