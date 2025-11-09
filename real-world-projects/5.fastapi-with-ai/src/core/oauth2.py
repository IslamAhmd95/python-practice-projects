from typing import Annotated

from fastapi import Depends, HTTPException, status # pyright: ignore[reportMissingImports]
from fastapi.security import OAuth2PasswordBearer  # pyright: ignore[reportMissingImports]
from sqlmodel import select, Session
from src.core.database import get_db

from src.models.user import User
from src.core.token import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token_str: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_access_token(token_str, credentials_exception)

    user = db.scalar(select(User).where(User.email == token_data.email))
    if user is None:
        raise credentials_exception

    return user