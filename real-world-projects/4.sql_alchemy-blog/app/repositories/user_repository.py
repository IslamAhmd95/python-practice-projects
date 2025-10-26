from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.user import User, RoleEnum
from app.models.profile import Profile
from app.schemas.user_schema import ReadUser, UpdatePassword
from app.core.hashing import hash_password, verify_password


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


def update_me(db: Session, user_id: int, data) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    

    try:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == "bio":
                if not user.profile:
                    user.profile = Profile(bio=value)
                else:
                    user.profile.bio = value
            else:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return {"message": "User updated successfully.", "user": ReadUser.model_validate(user)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the user.") from e


def update_password(db: Session, user_id: int, data: UpdatePassword) -> dict:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if not verify_password(data.current_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect.")
    
    try:
        user.password = hash_password(data.new_password)
        db.commit()
        return {"message": "Password updated successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the password.") from e
    

def get_all_users(db: Session, offset: int = 0, limit: int = 10) -> list[User]:
    return db.scalars(select(User).options(selectinload(User.profile)).where(User.role == RoleEnum.USER.value).offset(offset).limit(limit)).all()


def delete_user(db: Session, user_id: int) -> str:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    if user.role == RoleEnum.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete an admin user.")

    try:
        db.delete(user)
        db.commit()
        return {"message": f"User {user.username} deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the user.") from e

