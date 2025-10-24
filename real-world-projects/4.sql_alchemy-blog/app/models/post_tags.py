from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import BaseModel

class PostTag(BaseModel):
    __tablename__ = "posts_tags"

    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))