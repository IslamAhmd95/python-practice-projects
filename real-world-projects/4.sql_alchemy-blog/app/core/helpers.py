from fastapi import Depends, HTTPException, status  # pyright: ignore[reportMissingImports]
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user
from app.models.user import User
from app.core.enums import RoleEnum


def check_email_exists(email: str, db: Session):
    return db.execute(select(User).filter_by(email=email)).scalar()

def check_username_exists(username: str, db: Session):
    return db.execute(select(User).filter_by(username=username)).scalar()

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user