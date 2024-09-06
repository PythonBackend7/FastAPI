from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[Decimal] = None


class ItemUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[Decimal] = None


class ItemRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Optional[Decimal] = None

    class Config:
        orm_mode = True

