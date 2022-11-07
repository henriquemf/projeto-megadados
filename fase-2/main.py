from fastapi import FastAPI, HTTPException, Body, Query, status, Depends
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from dotenv import load_dotenv
import datetime

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
    return {"Página Inicial": "Bem vindo a API de estoque"}


#---------------------------------------------------------------------------------------------------------
#                                               INVENTORY
#---------------------------------------------------------------------------------------------------------



#---------------------------------GET ALL PRODUCTS---------------------------------#

@app.get("/inventory", tags=["Inventory"])
async def get_inventory(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

#--------------------------------GET BY SPECIFIC ID--------------------------------#

@app.get("/inventory/{product_id}", response_model=schemas.Product, tags=["Inventory"])
async def get_product(
    product_id: int = Query(
        title="Product ID",
        description="Select your desired Product by it's ID"
    ),
    db: Session = Depends(get_db)
):  
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    print(product)
    if product is None:
        raise HTTPException(status_code=400, detail="Product not found")
    return product



#--------------------------------CREATE NEW PRODUCT--------------------------------#

@app.post("/inventory/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED, tags=["Inventory"])
async def create_product(
    product: schemas.ProductCreate = Body(
        example={
            "name": "Apple", 
            "price": 1.99, 
            "description": "A red apple"
        }
    ),
    db: Session = Depends(get_db)
):
    db_product = models.Product(name=product.name, price=product.price, quantity=0, description=product.description)
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product data not valid")
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

#----------------------------------UPDATE PRODUCT----------------------------------#

### PUT ###
@app.put("/inventory/{product_id}", response_model=schemas.Product, tags=["Inventory"])
async def update_product_by_put(
    product_id: int = Query(
        title="Product ID",
        description="Select your desired Product by it's ID"
    ),
    product: schemas.ProductBase = Body(
        example={
            "name": "Apple", 
            "price": 1.99, 
            "description": "A red apple"
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
    db.commit()
    db.refresh(db_product)
    return db_product


### PATCH ###
@app.patch("/inventory/{product_id}", response_model=schemas.Product, tags=["Inventory"])
async def update_product_by_patch(
    product_id: int = Query(
        title="Product ID",
        description="Select your desired Product by it's ID"
    ),
    product_name: Optional[str] = Query(
        None,
        title="Product Name",
        description="Change Product name (not required)"
    ),
    product_price: Optional[float] = Query(
        None,
        title="Product Price",
        description="Change Product price (not required)"
    ),
    product_description: Optional[str] = Query(
        None,
        title="Product Description",
        description="Change Product description (not required)"
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
    db.commit()
    db.refresh(db_product)
    return db_product
    
#----------------------------------DELETE PRODUCT----------------------------------#

@app.delete("/inventory/{product_id}", tags=["Inventory"])
async def delete_product(
    product_id: int = Query(
        title="Product ID",
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

#---------------------------------------------------------------------------------------------------------
#                                                   MOV
#---------------------------------------------------------------------------------------------------------

#------------------------------------GET ALL MOVS----------------------------------#

@app.get("/movement", tags=["Movement"])
async def get_movement(db: Session = Depends(get_db)):
    return db.query(models.Movement).all()

#-------------------------------GET MOVEMENT BY SPECIFIC ID-----------------------------#

@app.get("/movement/{id_mov}", response_model=schemas.Movement, tags=["Movement"])
async def get_movement_by_id(
    id_mov: int = Query(
        title="Movement ID",
        description="Select the movement by it's ID"
    ),
    db: Session = Depends(get_db)
):  
    movement = db.query(models.Movement).filter(models.Movement.id == id_mov).first()
    if movement is None:
        raise HTTPException(status_code=400, detail="Movement not found")
    return movement

#----------------------------------CREATE NEW MOVEMENT----------------------------------#

@app.post("/movement/", response_model=schemas.Movement, status_code=status.HTTP_201_CREATED, tags=["Movement"])
async def create_movement(
    mov: schemas.MovementCreate = Body(
        example={
            "id_product": 1, 
            "quantity_change": 10,
        }
    ),
    db: Session = Depends(get_db)
):
    db_mov = models.Movement(id_product=mov.id_product, quantity_change=mov.quantity_change, date=datetime.datetime.now())
    if db_mov is None:
        raise HTTPException(status_code=400, detail="Movement data not valid")
    db_product = db.query(models.Product).filter(models.Product.id == db_mov.id_product).first()
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product ID not valid")
    if db_product.quantity + db_mov.quantity_change < 0:
        raise HTTPException(status_code=400, detail="Change makes Product Quantity be less than 0")
    try:
        db_product.quantity += db_mov.quantity_change
        db.add(db_mov)
        db.commit()
        db.refresh(db_mov)
        db.refresh(db_product)
    except:
        db.rollback()
    return db_mov

#----------------------------------UPDATE MOVEMENT----------------------------------#

### PATCH ###
@app.patch("/movement/{id_mov}", response_model=schemas.Movement, tags=["Movement"])
async def update_movement_by_patch(
    id_mov: int = Query(
        title="Movement ID",
        description="Select the movement by it's ID"
    ),
    quantity_change: Optional[int] = Query(
        None,
        title="Movement Quantity Change",
        description="Change movement quantity change (not required)"
    ),
    id_product: Optional[int] = Query(
        None,
        title="Product ID",
        description="Change movement product ID (not required)"
    ),

    db: Session = Depends(get_db)
):
    db_mov = db.query(models.Movement).filter(models.Movement.id == id_mov).first()
    if db_mov is None:
        raise HTTPException(status_code=400, detail="Movement ID not valid")

    db_product_old_mov = db.query(models.Product).filter(models.Product.id == db_mov.id_product).first()
        
    if id_product != None:
        db_product_new_mov = db.query(models.Product).filter(models.Product.id == id_product).first()
        if db_product_new_mov is None:
            raise HTTPException(status_code=400, detail="Product ID not valid")
        if quantity_change != None:
            new_quantity_change = quantity_change
        else:
            new_quantity_change = db_mov.quantity_change
        if db_product_old_mov.quantity - db_mov.quantity_change < 0:
            raise HTTPException(status_code=400, detail="Old movement can't be reversed")
        if db_product_old_mov.quantity - new_quantity_change < 0:
            raise HTTPException(status_code=400, detail="Can't apply movement because final product quantity is less than 0")
        try:
            db_product_old_mov.quantity -= db_mov.quantity_change
            db_product_new_mov.quantity += new_quantity_change
            if quantity_change != None:
                db_mov.quantity_change = quantity_change
            db_mov.id_product = id_product
            db.commit()
            db.refresh(db_mov)
            db.refresh(db_product_old_mov)
            db.refresh(db_product_new_mov)
        except:
            db.rollback()

    elif quantity_change != None:
        try:
            db_product_old_mov.quantity -= db_mov.quantity_change
            db_product_old_mov.quantity += quantity_change
            db_mov.quantity_change = quantity_change
            db.commit()
            db.refresh(db_mov)
            db.refresh(db_product_old_mov)
        except:
            db.rollback()
    
    return db_mov

#----------------------------------DELETE MOVEMENT----------------------------------#

@app.delete("/movement/{id_mov}", tags=["Movement"])
async def delete_movement(
    id_mov: int = Query(
        title="Movement ID",
        description="Select the movement by it's ID (needs to be the lastest done to the product)"
    ),
    db: Session = Depends(get_db)
):
    db_mov = db.query(models.Movement).filter(models.Movement.id == id_mov).first()
    if db_mov is None:
        raise HTTPException(status_code=400, detail="Movement ID not valid")
    db_product = db.query(models.Product).filter(models.Product.id == db_mov.id_product).first()
    db_product_last_mov = db.query(models.Movement).filter(models.Product.id == db_mov.id_product).order_by(models.Movement.id.desc()).first()
    if db_mov.id != db_product_last_mov.id:
        raise HTTPException(status_code=400, detail="This movement is not the last one made to this product, please delete in order from last to first.")
    try:
        db_product.quantity -= db_mov.quantity_change
        db.delete(db_mov)
        db.commit()
    except:
        db.rollback()
    return {"message": "Movement deleted successfully"}

#---------------------------------------------------------------------------------------------------------
#                                         MOV BY PRODUCT
#---------------------------------------------------------------------------------------------------------
#------------------------------GET MOVEMENT BY PRODUCT------------------------------#

@app.get("/movement/product/{id_product}", tags=["Movement by Product"])
async def get_movements_by_product(
    id_product: int = Query(
        title="Product ID",
        description="Select the product by it's ID (it will delete the last moviment done to the product)"
    ),
    db: Session = Depends(get_db)
):
    db_product = db.query(models.Product).filter(models.Product.id == id_product).first()
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product ID not valid")
    movements = db.query(models.Movement).filter(models.Movement.id_product == id_product).first()
    if movements is None:
        raise HTTPException(status_code=400, detail="No movements done to that product")
    return movements


#----------------------------DELETE MOVEMENT BY PRODUCT-----------------------------#
@app.delete("/movement/product/{id_product}", tags=["Movement by Product"])
async def delete_last_movement_by_product(
    id_product: int = Query(
        title="Product ID",
        description="Select the product by it's ID (it will delete the last moviment done to the product)"
    ),
    db: Session = Depends(get_db)
):
    db_product = db.query(models.Product).filter(models.Product.id == id_product).first()
    if db_product is None:
        raise HTTPException(status_code=400, detail="Product ID not valid")
    db_product_last_mov = db.query(models.Movement).filter(models.Product.id == id_product).order_by(models.Movement.id.desc()).first()
    if db_product_last_mov is None:
        raise HTTPException(status_code=400, detail="Product has no movements")
    try:
        db_product.quantity -= db_product_last_mov.quantity_change
        db.delete(db_product_last_mov)
        db.commit()
    except:
        db.rollback()
    return {"message": "Movement deleted successfully"}
