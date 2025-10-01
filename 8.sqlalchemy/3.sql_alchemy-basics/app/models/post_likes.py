from sqlalchemy import Table, Column, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import BaseModel

post_likes = Table("post_likes", BaseModel.metadata,
                Column('user_id', ForeignKey("users.id", ondelete = "CASCADE", onupdate = "CASCADE"), primary_key=True), 
                Column('post_id', ForeignKey("posts.id", ondelete = "CASCADE", onupdate = "CASCADE"), primary_key=True), 
                Column('created_at', DateTime, server_default=func.now()), 
                Column('updated_at', DateTime, onupdate=func.now())
            )