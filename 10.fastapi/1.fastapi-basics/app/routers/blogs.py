from typing import List
from fastapi import APIRouter, Depends, status  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Blog, ShowBlogWithUser, UpdateBlog
from ..repositories.blog_repository import *
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/blogs", tags=['Blogs']
)


# get all blogs
@router.get('/', response_model=List[ShowBlogWithUser])
def all(db: Session = Depends(get_db)):
    return get_all(db)


# create a blog
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create(request, db, current_user)

# show a blog with id
@router.get('/{id}', response_model=ShowBlogWithUser)
def show_blog(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return show(id, db)

# update a blog
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: UpdateBlog, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update(id, request, db)

# delete a blog
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return destroy(id, db)
