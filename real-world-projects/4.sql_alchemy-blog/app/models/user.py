from app.database import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column, foreign
from .user_followers import user_followers
from .comment_likes import comment_likes
from .post_likes import post_likes


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)

    profile = relationship("Profile", cascade="all, delete-orphan", back_populates="user", single_parent=True, uselist=False, lazy="joined")
    posts = relationship("Post", lazy="select", cascade="all, delete-orphan", backref="user")
    comments = relationship("Comment", cascade="all, delete-orphan", back_populates="user")
    following = relationship("User", secondary=user_followers,
                            primaryjoin=lambda: foreign(user_followers.c.follower_id) == User.id,
                            secondaryjoin=lambda: foreign(user_followers.c.following_id) == User.id
                            )
    liked_comments = relationship(
        "Comment",
        secondary=comment_likes,
        back_populates="liked_by"
    )
    liked_posts = relationship(
        "Post",
        secondary=post_likes,
        back_populates="liked_by"
    )


    
    def __repr__(self):
        return f"User(name={self.name}, username={self.username})"