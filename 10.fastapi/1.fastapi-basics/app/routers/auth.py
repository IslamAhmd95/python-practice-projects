from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Form # pyright: ignore[reportMissingImports]
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Login, ShowUserWithToken
from app.hashing import Hash
from app.models import UserModel
from app.token  import *


router = APIRouter(
    tags=["Auth"]
)


@router.post('/login', response_model=ShowUserWithToken)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    data = Login(username=username, password=password)

    user = db.scalar(select(UserModel).where(UserModel.email == data.username))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not Hash.verify(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    
    # generate a jwt and return it
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {**user.__dict__, "access_token": access_token, "token_type": "bearer"}