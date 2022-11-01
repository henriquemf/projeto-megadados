from fastapi import FastAPI, HTTPException, Path, Body, Query, status
from typing import Union, Optional

from pydantic import BaseModel

app = FastAPI()
class Product(BaseModel):
    name: str
    price: float
    description: Union[str, None] = None
    quantity: int

maca = Product(name = "Apple", price = 1.99, description = "A red apple", quantity = 10)
laranja = Product(name = "Orange", price = 2.99, description = "A orange", quantity = 20)
banana = Product(name = "Banana", price = 3.99, description = "A banana", quantity = 30)

inventory = {0:maca, 1:laranja, 2:banana}

#-----------------------------------STARTING PAGE----------------------------------#

@app.get("/")
def read_root():
    return {"Página Inicial": "Bem vindo a API de estoque, caminhos disponíveis: '/inventory' para GET e POST , '/inventory/{product_id}' para GET, PUT, PATCH e DELETE"}

#---------------------------------GET ALL PRODUCTS---------------------------------#

@app.get("/inventory")
async def get_inventory():
    return inventory

#--------------------------------GET BY SPECIFIC ID--------------------------------#

@app.get("/inventory/{product_id}", status_code = 200, response_model_exclude_unset = True)
async def get_product(
    product_id: int = Path(
        title="Product ID",
        description="Select your desired Product by it's ID", 
        gt = -1, 
        le = len(inventory)-1
    )
):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product_id, "product": inventory[product_id]}

# @app.get("/inventory/{product_id}", status_code = 200, response_model = Product, response_model_exclude_unset = True)
# async def get_product(product_id: int = Path(..., gt = -1, le = len(inventory)-1)):
#     if product_id in inventory:
#         return inventory[product_id]
#     else:
#         raise HTTPException(status_code = 404, detail = "Product not found")

#--------------------------------CREATE NEW PRODUCT--------------------------------#

@app.post("/inventory/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: Product = Body(
        example={
            "name": "Apple", 
            "price": 1.99, 
            "description": "A red apple", 
            "quantity": 10
        }
    )
):
    inventory[len(inventory)] = product
    return {"product_id": len(inventory)-1, "product": inventory[len(inventory)-1]}

#----------------------------------UPDATE PRODUCT----------------------------------#

### PUT ###
@app.put("/inventory/{product_id}")
async def update_product_by_put(
    product_id: int = Path(
        alias="Product ID",
        description="Select your desired Product by it's ID"
    ),
    product: Product = Body(
        example={
            "name": "Apple", 
            "price": 1.99, 
            "description": "A red apple", 
            "quantity": 10
        }
    )
):
    if product_id not in inventory.keys():
        raise HTTPException(status_code=404, detail="Product not found")
    inventory[product_id] = product
    return {"product_id": product_id, "product": inventory[product_id]}

### PATCH ###
@app.patch("/inventory/{product_id}")
async def update_product_by_patch(
    product_id: int = Path(
        alias="Product ID",
        description="Select your desired Product by it's ID"
    ),
    product_name: Optional[str] = Query(
        None,
        alias="Product Name",
        description="Rodrigo Gostoso S2 Change Product name (not required)"
    ),
    product_price: Optional[float] = Query(
        None,
        alias="Product Price",
        description="Change Product price (not required)"
    ),
    product_description: Optional[str] = Query(
        None,
        alias="Product Description",
        description="Change Product description (not required)"
    ),
    product_quantity: Optional[int] = Query(
        None,
        alias="Product Quantity",
        description="Change Product quantity (not required)"
    )
):
    if product_id not in inventory.keys():
        raise HTTPException(status_code=404, detail="Product not found")
    if product_name != None:
        inventory[product_id].name = product_name
    if product_price != None:
        inventory[product_id].price = product_price
    if product_description != None:
        inventory[product_id].description = product_description
    if product_quantity != None:
        inventory[product_id].quantity = product_quantity
    return {"product_id": product_id, "product": inventory[product_id]}
    
#----------------------------------DELETE PRODUCT----------------------------------#

@app.delete("/inventory/{product_id}")
async def delete_product(
    product_id: int = Path(
        alias="Product ID",
        description="Select your desired Product by it's ID"
    )
):
    if product_id not in inventory.keys():
        raise HTTPException(status_code=404, detail="Product not found")
    temp = inventory[product_id]
    del inventory[product_id]
    return {"product_id": product_id, "product": temp}
