from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field   

from app.core.enums import OrderEnum


class ResponseBaseSchema(BaseModel):
    message: str


class TagFilterSchema(BaseModel):
    offset: int = 0
    limit: int = 10
    order: OrderEnum = OrderEnum.ASC


class ReadPostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class ReadTagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    posts: List[ReadPostSchema] = Field(default_factory=list)


class TagPaginationSchema(BaseModel):
    tags: list[ReadTagSchema]
    total: int
    page: int
    limit: int


class CreateTagSchema(BaseModel):
    name: str


class AfterCreateTagSchema(ResponseBaseSchema):
    tag: ReadTagSchema


class UpdateTagSchema(BaseModel):
    name: str


class AfterUpdateTagSchema(ResponseBaseSchema):
    tag: ReadTagSchema


class AfterDeleteTagSchema(ResponseBaseSchema):
    pass