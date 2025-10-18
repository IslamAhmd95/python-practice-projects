from typing import Annotated

from fastapi import Depends, HTTPException, status # pyright: ignore[reportMissingImports]
from fastapi.security import OAuth2PasswordBearer  # pyright: ignore[reportMissingImports]
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db

from app.models import UserModel
from .token import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(tokenData: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_access_token(tokenData, credentials_exception)

    user = db.scalar(select(UserModel).where(UserModel.email == token_data.email))
    if user is None:
        raise credentials_exception

    return user