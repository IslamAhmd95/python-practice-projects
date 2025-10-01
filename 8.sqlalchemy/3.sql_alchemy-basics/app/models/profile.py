from app.database import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Profile(BaseModel):
    __tablename__ = "profiles"

    bio: Mapped[str] = mapped_column(Text)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), unique=True)

    user = relationship("User", back_populates="profile")
