from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    description = Column(String(500), nullable=True, index=True)
    quantity = Column(Integer, nullable=False, index=True)

    movement = relationship("Movement", back_populates="product", cascade="all, delete")

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    id_product = Column(Integer, ForeignKey("products.id"))
    quantity_change = Column(Integer, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)

    product = relationship("Product", back_populates="movement")


    