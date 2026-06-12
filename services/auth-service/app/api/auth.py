from fastapi import APIRouter, HTTPException

from app.clients.user_client import get_user_by_email
from app.core.security import create_access_token
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


@router.post("/login")
def login(email: str, password: str):

    user = get_user_by_email(email)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not pwd_context.verify(password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"sub": str(user["id"])}
    )

    return {"access_token": token}