from sqlalchemy import Column, Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    description = Column(String(500), nullable=True, index=True)
    quantity = Column(Integer, nullable=False, index=True)




    