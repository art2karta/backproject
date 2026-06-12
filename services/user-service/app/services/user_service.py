from sqlalchemy.orm import Session
from app.db.models import User


def create_user(
    db: Session,
    email: str,
    password_hash: str,
):
    user = User(
        email=email,
        password_hash=password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_email(
    db,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )