
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User, RoleEnum
from app.models.profile import Profile


def get_all_users(db: Session):
    return db.scalars(select(User).where(User.role == RoleEnum.USER.value))