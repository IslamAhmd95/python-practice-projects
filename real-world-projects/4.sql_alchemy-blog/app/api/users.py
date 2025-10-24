from fastapi import APIRouter, Depends # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories import user_repository
from app.schemas.user_schema import ReadUser
from app.core.helpers import admin_required


router = APIRouter(
    prefix="/users", tags=["Users"]
)

@router.get('/', dependencies=[Depends(admin_required)], response_model=list[ReadUser])
def get(db: Session = Depends(get_db)):
    return user_repository.get_all_users(db)

