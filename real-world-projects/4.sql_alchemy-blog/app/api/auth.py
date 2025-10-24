from typing import Optional

from fastapi import APIRouter, Depends, status, Form, HTTPException   # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.core.database import get_db
from app.repositories import auth_repository
from app.schemas.auth_schema import (SignUpSchema, LoginSchema, AfterSignUpSchema, AfterLoginSchema)


router = APIRouter(
    prefix="/auth", tags=["Auth"]
)


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=AfterSignUpSchema)
def sign_up(data: SignUpSchema, db: Session = Depends(get_db)):
    return auth_repository.signup(data, db)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=AfterLoginSchema)
def login(
    username: str | None = Form(None),
    email: EmailStr | None = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if not username and not email:
        raise HTTPException(status_code=400, detail="Username or email required")
    
    schema = LoginSchema(login=username or email, password=password)
    return auth_repository.login(schema, db)

