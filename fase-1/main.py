from fastapi import FastAPI, HTTPException
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

inventory = {0:maca, 1:laranja, 2:banana}

@app.get("/items")
async def get_inventory():
    return inventory

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in inventory.keys():
        raise HTTPException(status_code=404, detail="Item not found")
    result = inventory[item_id]
    return {"item_id": item_id, "item": result,}

@app.post("/items/")
async def create_item(item: Item):
    inventory[len(inventory)] = item
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in inventory.keys():
        raise HTTPException(status_code=404, detail="Item not found")
    inventory[item_id] = item
    return inventory[item_id]

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in inventory.keys():
        raise HTTPException(status_code=404, detail="Item not found")
    del inventory[item_id]
    return inventory

