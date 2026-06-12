from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from fastapi import HTTPException
from app.db.database import SessionLocal
from app.core.security import hash_password

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

from app.services.user_service import (
    create_user,
    get_user_by_email,
)
@router.post(
    "/users",
    response_model=UserResponse,
)
def create_user_endpoint(
    payload: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = get_user_by_email(
        db,
        payload.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    user = create_user(
        db=db,
        email=payload.email,
        password_hash=hash_password(
            payload.password
        ),
    )
    print("HASH FUNCTION USED")

    return user