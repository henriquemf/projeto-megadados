from pydantic import BaseModel
from typing import Union

class ProductBase(BaseModel):
    name: str
    price: float
    description: Union[str, None] = None
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True