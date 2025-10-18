from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Response  # pyright: ignore[reportMissingImports]
from ..database import get_db
from ..schemas import Blog
from ..models import BlogModel, UserModel


def create(request: Blog, db: Session, current_user: UserModel):
    new_blog = BlogModel(**request.model_dump(), user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": f"Blog is created with id as {new_blog.id}"}


def show(id: int, db: Session = Depends(get_db)):
    blog = db.scalar(select(BlogModel).where(BlogModel.id == id))
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    return blog


def get_all(db: Session = Depends(get_db)):
    return db.scalars(select(BlogModel)).all()


def update(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.scalar(select(BlogModel).where(BlogModel.id == id))
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.title = request.title
    blog.body = request.body
    blog.published = request.published

    db.commit()
    db.refresh(blog)
    return {"data": f"Blog with id {id} has been updated"}


def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.scalar(select(BlogModel).where(BlogModel.id == id))
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)