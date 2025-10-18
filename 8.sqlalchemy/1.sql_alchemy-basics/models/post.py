from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.base import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    # from sqlalchemy.ord import defer
    # content = defer(Column(TEXT, nullable=False))
    content: Mapped[TEXT] = mapped_column(nullable=False, deferred=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    author = relationship("User", back_populates="posts")  # back_populates means: keep both sides in sync.

    liked_by = relationship(
        "User",
        secondary="likes",  # refers to the association table defined in like.py
        back_populates="liked_posts"  # back_populates ensures both sides (User ↔ Post) stay in sync.
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title}, user_id={self.user_id})>"