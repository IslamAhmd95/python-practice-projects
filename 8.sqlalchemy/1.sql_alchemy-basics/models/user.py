"""
Purpose: define your tables (ORM models).
They import Base from db/base.py.
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")  # back_populates means: keep both sides in sync.
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")  # one-to-one relationship, uselist=False means single object not a list.

    liked_posts = relationship(
        "Post",
        secondary="likes",  # refers to the association table defined in like.py
        back_populates="liked_by",  # back_populates ensures both sides (User ↔ Post) stay in sync.
        cascade="all"
    )


    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
        # return dict(id=self.id, username=self.username, email=self.email).__repr__()




"""
Explanation:

    - Column: defines a column in a database table.

    - Integer and String: data types for the columns.

    - Base: the base class from db/base.py. All models must inherit from it.

    - class User(Base): we create a model class named User. It represents a table in the DB.

        - __tablename__ = "users": tells SQLAlchemy that this class maps to a table called users.

        - id: a column in the table.

        - Integer: the type is integer.

        - primary_key=True: this column uniquely identifies each row.

        - index=True: create a database index on this column for faster searches.
"""