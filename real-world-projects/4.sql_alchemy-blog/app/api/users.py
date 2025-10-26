from fastapi import APIRouter, Depends # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories import user_repository
from app.schemas.user_schema import ReadUser, AfterDeleteUser, UpdateMe, AfterUpdateMe, UpdatePassword, AfterUpdatePassword
from app.core.helpers import admin_required, get_current_user


router = APIRouter(
    prefix="/users", tags=["Users"]
)



@router.get('/me', response_model=ReadUser)
def show_me(current_user: ReadUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_repository.get_user_by_id(db, current_user.id)


@router.put('/me', response_model=AfterUpdateMe)
def update_me(data: UpdateMe, current_user: ReadUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_repository.update_me(db, current_user.id, data)


@router.put('/me/update-password', response_model=AfterUpdatePassword)
def update_password(data: UpdatePassword, current_user: ReadUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_repository.update_password(db, current_user.id, data)


@router.get('/', dependencies=[Depends(admin_required)], response_model=list[ReadUser])
def get_all_users(offset: int = 0, limit:int = 10, db: Session = Depends(get_db)):
    return user_repository.get_all_users(db, offset=offset, limit=limit)


@router.get('/{user_id}', response_model=ReadUser)
def show(user_id: int, db: Session = Depends(get_db)):
    return user_repository.get_user_by_id(db, user_id)


@router.delete('/{user_id}', dependencies=[Depends(admin_required)], response_model=AfterDeleteUser)
def delete(user_id: int, db: Session = Depends(get_db)):
    return user_repository.delete_user(db, user_id)
