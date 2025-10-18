from fastapi import APIRouter, Depends, HTTPException, status # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import User, ShowUserWithBlogs
from ..repositories.user_repository import *

router = APIRouter(
    prefix="/users", tags=['Users']
)


# create a user
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)):
    return create(request, db)

# show a user with id
@router.get('/{id}', response_model=ShowUserWithBlogs)
def show_user(id: int, db: Session = Depends(get_db)):
    return show(id, db)

# delete a user
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    return destroy(id, db)