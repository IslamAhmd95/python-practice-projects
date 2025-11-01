from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import OrderEnum
from app.schemas.comment_schema import CommentSchema


class ResponseBaseSchema(BaseModel):
    message: str


class PostFilterSchema(BaseModel):
    offset: int = 0
    limit: int = 10
    order: OrderEnum = OrderEnum.ASC


class CommentFilterSchema(BaseModel):
    offset: int = 0
    limit: int = 10
    order: OrderEnum = OrderEnum.ASC


class AuthorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str


class ReadTagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user: AuthorSchema
    tags: List[ReadTagSchema] = Field(default_factory=list)


class ReadOnePostSchema(BaseModel):
    post: PostSchema


class ReadPostSchema(BaseModel):
    posts: List[PostSchema] = Field(default_factory=list)
    total: int
    page: int
    limit: int


class ReadCommentsSchema(BaseModel):
    comments: list[CommentSchema] = Field(default_factory=list)
    total: int
    page: int
    limit: int


class CreatePostSchema(BaseModel):
    title: str
    content: str
    tag_ids: Optional[List[int]] = Field(default_factory=list)


class CreateCommentSchema(BaseModel):
    content: str

    
class UpdatePostSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tag_ids: Optional[List[int]] = Field(default_factory=list)


class AfterCreatePostSchema(ResponseBaseSchema):
    post: PostSchema


class AfterCreateCommentSchema(ResponseBaseSchema):
    comment: CommentSchema


class AfterUpdatePostSchema(ResponseBaseSchema):
    post: PostSchema


class AfterDeletePostSchema(ResponseBaseSchema):
    pass


class LikeResponseSchema(BaseModel):
    message: str


class GetPostLikesSchema(BaseModel):
    total_likes: int
    liked_users: List[AuthorSchema] = Field(default_factory=list)