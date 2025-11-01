from typing import List
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import OrderEnum


class ResponseSchema(BaseModel):
    message: str


class AuthorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str


class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class CommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    user: AuthorSchema
    post: PostSchema


class ReadCommentSchema(BaseModel):
    comment: CommentSchema


class UpdateCommentSchema(BaseModel):
    content: str


class AfterUpdateCommentSchema(ResponseSchema):
    comment: CommentSchema


class AfterDeleteCommentSchema(ResponseSchema):
    pass


class LikeCommentSchema(ResponseSchema):
    pass


class GetCommentLikesSchema(BaseModel):
    total_likes: int
    liked_users: List[AuthorSchema] = Field(default_factory=list)