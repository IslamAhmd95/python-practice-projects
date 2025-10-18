from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status  # pyright: ignore[reportMissingImports]
from ..database import get_db
from ..schemas import User
from ..models import UserModel
from ..hashing import Hash


def create(request: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = UserModel(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": f"User is created with id as {new_user.id}"}


def show(id: int, db: Session = Depends(get_db)):
    user = db.scalar(select(UserModel).where(UserModel.id == id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

def destroy(id: int, db: Session = Depends(get_db)):
    user = db.scalar(select(UserModel).where(UserModel.id == id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return {"data": f"User with id {id} has been deleted"}