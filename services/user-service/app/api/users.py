from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from app.services.user_service import create_user

from app.db.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/users",
    response_model=UserResponse,
)
def create_user_endpoint(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    user = create_user(
        db=db,
        email=payload.email,
        password_hash=payload.password,
    )

    return user