from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.order_model import OrderItem, Order
from typing import Optional
from datetime import datetime


# Get All Products from the Database
def get_all_products(session: Session):
    all_products = session.exec(select(Product)).all()
    return all_products

# Get product by ID from Database
def get_product_by_id(product_id: int, session: Session):
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
