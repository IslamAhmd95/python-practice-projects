from sqlalchemy import Integer, String, Text, Column, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class BlogModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    published = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))

    creator = relationship("UserModel", back_populates="blogs")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    blogs = relationship("BlogModel", back_populates="creator", cascade="all, delete-orphan")