from fastapi import FastAPI

from app.db.database import Base
from app.db.database import engine

from .api.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)


@app.get("/health")
def health():
    return {"status": "ok"}