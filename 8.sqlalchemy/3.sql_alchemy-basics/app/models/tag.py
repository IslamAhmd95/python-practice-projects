from app.database import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Tag(BaseModel):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    