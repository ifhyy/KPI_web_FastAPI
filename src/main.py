from fastapi import FastAPI
from src import models
from src.database import engine, SessionLocal


models.Model.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
