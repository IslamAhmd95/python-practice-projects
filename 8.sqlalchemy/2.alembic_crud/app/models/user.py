from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"UserModel(id={self.id}, name={self.name}, email={self.email})"