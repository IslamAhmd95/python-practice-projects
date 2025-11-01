from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import BaseModel


class Tag(BaseModel):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    posts: Mapped[list["Post"]] = relationship(secondary="posts_tags", back_populates="tags")  # pyright: ignore[reportUndefinedVariable]

    def __repr__(self) -> str:
        return f"Tag(name={self.name})"
