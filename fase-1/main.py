from fastapi import FastAPI
from typing import Union

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    item_name: str
    item_price: float
    item_description: Union[str, None] = None
    item_quantity: int

maca = Item(item_name = "Apple", item_price = 1.99, item_description = "A red apple", item_quantity = 10)
laranja = Item(item_name = "Orange", item_price = 2.99, item_description = "A orange", item_quantity = 20)
banana = Item(item_name = "Banana", item_price = 3.99, item_description = "A banana", item_quantity = 30)

listaItens = {0:maca, 1:laranja, 2:banana}

@app.get("/items")
async def get_items():
    return listaItens

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    result = listaItens[item_id-1]
    return {"item_id": item_id, "item": result,}
