from fastapi import APIRouter, Depends, status, Form, HTTPException   # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.core.database import get_db
from app.repositories import auth_repository
from app.schemas.auth_schema import (
    SignUpSchema, LoginSchema, AfterSignUpSchema, AfterLoginSchema, UserReadSchema
)


router = APIRouter(
    prefix="/auth", tags=["Auth"]
)


@router.post('/register', response_model=AfterSignUpSchema, status_code=status.HTTP_201_CREATED)
def sign_up(data: SignUpSchema, db: Session = Depends(get_db)):
    user = auth_repository.signup(data, db)
    return {"user": user, "message": "User created successfully"}


@router.post('/login', response_model=AfterLoginSchema, status_code=status.HTTP_200_OK)
def login(
    username: str | None = Form(None),
    email: EmailStr | None = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if not username and not email:
        raise HTTPException(status_code=400, detail="Username or email required")
    
    schema = LoginSchema(login=username or email, password=password)
    user, access_token = auth_repository.login(schema, db)
    
    return {"user": UserReadSchema.model_validate(user), "access_token": access_token, "token_type": "bearer"}

