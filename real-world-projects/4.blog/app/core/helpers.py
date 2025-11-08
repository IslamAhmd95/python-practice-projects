from typing import Optional

from fastapi import Depends, HTTPException, status  # pyright: ignore[reportMissingImports]
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user
from app.models.user import User
from app.core.enums import RoleEnum


def check_email_exists(email: str, db: Session, user: Optional[User] = None):
    query = select(User).where(User.email == email)
    if user:
        query = query.where(User.id != user.id)

    return db.execute(query).scalar()

def check_username_exists(username: str, db: Session, user: Optional[User] = None):
    query = select(User).where(User.username == username)
    if user:
        query = query.where(User.id != user.id)

    return db.execute(query).scalar()

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user