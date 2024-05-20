from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None


class Item(ItemBase):
    id: int
    location: "Location"
    category: "Category"

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    location_id: int
    category_id: int


class LocationBase(BaseModel):
    name: str


class Location(LocationBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True


class LocationCreate(LocationBase):
    pass


class CategoryBase(BaseModel):
    name: str


class Category(CategoryBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


Item.update_forward_refs()
Location.update_forward_refs()
Category.update_forward_refs()
