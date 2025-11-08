from sqlalchemy import Table, Column, Integer, ForeignKey

from app.core.database import BaseModel


user_followers = Table("user_followers", BaseModel.metadata,
                Column('follower_id', Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
                Column('following_id', Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
            )
            