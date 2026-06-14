from fastapi import FastAPI

from app.db.database import engine
from app.db.database import Base

import app.db.models


app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}