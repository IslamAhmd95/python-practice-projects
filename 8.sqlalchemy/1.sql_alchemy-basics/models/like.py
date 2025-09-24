from sqlalchemy import Table, Column, Integer, ForeignKey
from db.base import Base    


# Association table for many-to-many relationship between users and posts they liked.

like_table = Table(
    "likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
)





"""
Notes:

    - For a pure association table (just foreign keys, no extra columns), you don’t need to create a full class model.

    - Just defining it as a Table(...) (like we did with likes) is enough.

    - Because it’s defined with Base.metadata, it will be included when you call:
        Base.metadata.create_all(bind=engine)
        in app.ipynb
"""