from app.database import BaseModel
from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .post_likes import post_likes


class Post(BaseModel):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    # from sqlalchemy.ord import defer
    # content = defer(Column(TEXT, nullable=False))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))

    tags = relationship("Tag", secondary="posts_tags", backref="posts")
    comments = relationship("Comment", cascade="all, delete-orphan", backref="post")
    liked_by = relationship(
        "User",
        secondary=post_likes,
        back_populates="liked_posts"
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title}, user_id={self.author_id})>"
