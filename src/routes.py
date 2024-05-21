from fastapi import APIRouter, Depends, HTTPException, status, Response
from src.schemas import (Item, ItemCreate, ItemUpdate,
                         Category, CategoryCreate, CategoryUpdate,
                         Location, LocationCreate, LocationUpdate)
from sqlalchemy.orm import Session
from src.database import get_db
from src import models

item_router = APIRouter(prefix="/items", tags=["Items"])
category_router = APIRouter(prefix="/categories", tags=["Categories"])
location_router = APIRouter(prefix="/locations", tags=["Locations"])


def validate_location_id(location_id: int, db: Session):
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=400, detail="Invalid location_id")
    return location

def validate_category_id(category_id: int, db: Session):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    return category


@item_router.get("/", response_model=list[Item])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items


@item_router.get("/{id}/", response_model=Item)
def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@item_router.post("/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    validate_category_id(item.category_id, db)
    validate_location_id(item.location_id, db)
    new_item = models.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@item_router.patch("/{id}", response_model=Item)
def update_item(id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    update_data = item_update.dict(exclude_unset=True)
    if update_data['location_id']:
        validate_location_id(update_data['location_id'], db)

    if update_data['category_id']:
        validate_category_id(update_data['category_id'], db)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@item_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@category_router.get("/", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories


@category_router.get("/{id}/", response_model=Category)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@category_router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Item(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@category_router.patch("/{id}", response_model=Category)
def update_category(id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_data = category_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@category_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@location_router.get("/", response_model=list[Location])
def get_location(db: Session = Depends(get_db)):
    locations = db.query(models.Location).all()
    return locations


@location_router.get("/{id}/", response_model=Location)
def get_location(id: int, db: Session = Depends(get_db)):
    location = db.query(models.Location).filter(models.Location.id == id).first()
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


@location_router.post("/", response_model=Location)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    new_location = models.Location(**location.model_dump())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


@location_router.patch("/{id}", response_model=Location)
def update_location(id: int, location_update: LocationUpdate, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == id).first()
    if not db_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_data = location_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location


@location_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == id).first()
    if not db_location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
