from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import BaseModel

class PostTag(BaseModel):
    __tablename__ = "posts_tags"
    __table_args__ = (UniqueConstraint('post_id', 'tag_id', name='uq_post_tag'),)

    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"), primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), primary_key=True)