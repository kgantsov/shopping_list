from typing import List
from enum import Enum

from pydantic import BaseModel


class Unit(str, Enum):
    kg = "kg"
    box = "box"


class ShoppingListSchema(BaseModel):
    id: int = 0
    name: str
    description: str = None


class ShoppingItemSchema(BaseModel):
    id: int = 0
    name: str
    description: str = None
    quantity: int
    unit: Unit = None
    done: bool = False


class ShoppingItemsSchema(BaseModel):
    shopping_list: ShoppingListSchema
    objects: List[ShoppingItemSchema]
