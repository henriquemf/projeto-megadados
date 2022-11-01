from fastapi import FastAPI, HTTPException, Path, Body, Query, status, Depends
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#-----------------------------------STARTING PAGE----------------------------------#

@app.get("/")
def read_root():
    return {"Página Inicial": "Bem vindo a API de estoque, caminhos disponíveis: '/inventory' para GET e POST , '/inventory/{product_id}' para GET, PUT, PATCH e DELETE"}

#---------------------------------GET ALL PRODUCTS---------------------------------#

@app.get("/inventory")
async def get_inventory(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

#--------------------------------GET BY SPECIFIC ID--------------------------------#

@app.get("/inventory/{product_id}", response_model=schemas.Product)
async def get_product(
    product_id: int = Query(
        alias="Product ID",
        description="Select your desired Product by it's ID"
    ),
    db: Session = Depends(get_db)
):  
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    print(product)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



#--------------------------------CREATE NEW PRODUCT--------------------------------#

@app.post("/inventory/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: schemas.ProductCreate = Body(
        example={
            "name": "Apple", 
            "price": 1.99, 
            "description": "A red apple", 
            "quantity": 10
        }
    ),
    db: Session = Depends(get_db)
):
    db_product = models.Product(name=product.name, price=product.price, quantity=product.quantity, description=product.description)
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product data not valid")
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

#----------------------------------UPDATE PRODUCT----------------------------------#

### PUT ###
@app.put("/inventory/{product_id}", response_model=schemas.Product)
async def update_product_by_put(
    product_id: int = Query(
        alias="Product ID",
        description="Select your desired Product by it's ID"
    ),
    product: schemas.ProductBase = Body(
        example={
            "name": "Apple", 
            "price": 1.99, 
            "description": "A red apple", 
            "quantity": 10
        }
    ),
    db: Session = Depends(get_db)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product ID not valid")
    db_product.name = product.name
    db_product.price = product.price
    db_product.description = product.description
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product


### PATCH ###
@app.patch("/inventory/{product_id}", response_model=schemas.Product)
async def update_product_by_patch(
    product_id: int = Query(
        alias="Product ID",
        description="Select your desired Product by it's ID"
    ),
    product_name: Optional[str] = Query(
        None,
        alias="Product Name",
        description="Change Product name (not required)"
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
    ),
    db: Session = Depends(get_db)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product ID not valid")
    if product_name != None:
        db_product.name = product_name
    if product_price != None:
        db_product.price = product_price
    if product_description != None:
        db_product.description = product_description
    if product_quantity != None:
        db_product.quantity = product_quantity
    db.commit()
    db.refresh(db_product)
    return db_product
    
#----------------------------------DELETE PRODUCT----------------------------------#

@app.delete("/inventory/{product_id}", response_model=schemas.Product)
async def delete_product(
    product_id: int = Query(
        alias="Product ID",
        description="Select your desired Product by it's ID"
    ),
    db: Session = Depends(get_db)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product ID not valid")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

