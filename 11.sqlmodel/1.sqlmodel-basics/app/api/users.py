from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


SessionDep = Annotated[Session, Depends(get_db)]
limitType = Annotated[int, Query(le=10)]

@router.get("/", response_model=list[UserRead])
def get_users(db: SessionDep, limit: limitType = 10, offset: int = 0):
    return db.exec(select(User).offset(offset).limit(limit)).all()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: SessionDep):
    user = User.model_validate(data)  #  The User model has the model_validate method because it inherits from SQLModel, which itself inherits from Pydantic's BaseModel.


    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected server error occurred: {str(e)}"
        )


@router.get('{user_id}', response_model=UserRead)
def read_user(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    return user


@router.patch("/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    
    if data.email is not None and data.email != user.email:
        existing_user = db.scalar(select(User).where(User.email == data.email, User.id != user.id))
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists for another user"
            )

    # Use Pydantic's model_dump(exclude_unset=True) to get only provided fields
    user_data = data.model_dump(exclude_unset=True, exclude_none=True) 
    # return {"type": str(type(user_data)), "data": user_data}   # Dict type

    # Use SQLModel's update method, Updates only the fields provided in the patch request.
    user.sqlmodel_update(user_data)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    # UserUpdate (Pydantic) → partial dict → sqlmodel_update → SQLAlchemy tracks → DB UPDATE
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"DB error occurred: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected server error occurred: {str(e)}"
        )
    

@router.delete('/{user_id}')
def delete_user(user_id: int, db: SessionDep):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user.name} has been deleted."}