from fastapi import FastAPI
from . import models
from .database import engine, SessionLocal


models.Model.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
