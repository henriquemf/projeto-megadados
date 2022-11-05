from datetime import datetime
from pydantic import BaseModel, Field
from typing import Union

class ProductBase(BaseModel):
    name: str = Field(title="Product Name")
    price: float = Field(default=None, title="Product Price")
    description: Union[str, None] = Field(default=None, title="Product Description")

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    quantity: int = Field(default=0, title="Product Quantity")
    class Config:
        orm_mode = True


class MovementBase(BaseModel):
    quantity_change: int = Field(title="Variation quantity")
    id_product: int = Field(title="Product ID")

class MovementCreate(MovementBase):
    pass
    
class Movement(MovementBase):
    id: int
    date: datetime = Field(title="Date & Time of creation or update")

    class Config:
        orm_mode = True