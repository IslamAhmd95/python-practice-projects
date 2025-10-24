from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import BaseModel
from app.models.comment_likes import comment_likes


class Comment(BaseModel):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE"))

    user = relationship("User", back_populates="comments")
    liked_by = relationship(
        "User",
        secondary=comment_likes,
        back_populates="liked_comments"
    )

