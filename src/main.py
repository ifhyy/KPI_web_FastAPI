from fastapi import FastAPI
from src.routes import item_router, location_router, category_router


# models.Model.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(item_router)
app.include_router(category_router)
app.include_router(location_router)

