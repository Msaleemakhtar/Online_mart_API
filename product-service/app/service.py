from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.product_model import Product,Category, ProductRating, ProductRatingCreate,ProductUpdate
from typing import Optional
from datetime import datetime
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add product in database
def create_product(db: Session, product: ProductUpdate) -> Product:
    # Check if the category exists
    category = db.exec(select(Category).where(Category.id == product.category_id)).first()
    if not category:
        new_category = Category(id=product.category_id, name=f"Category {product.category_id}")
        db.add(new_category)
        db.commit()
        logger.info(f"Category created: {new_category}")
        
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        expiry=product.expiry,
        brand=product.brand,
        weight=product.weight,
        category_id=product.category_id,
        sku=product.sku,
        stock_quantity=product.stock_quantity,
        reorder_level=product.reorder_level,
        meta_title=product.meta_title,
        meta_description=product.meta_description,
        meta_keywords=product.meta_keywords
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product





#update product in database
def update_product(product_id: int, product: ProductUpdate, db: Session):
    # Fetch the existing product from the database
    existing_product = db.exec(select(Product).where(Product.id == product_id)).first()
    
    if existing_product:
        # Update only the fields that are present in the message
        if product.name:
            existing_product.name = product.name
        if product.description:
            existing_product.description = product.description
        if product.price:
            existing_product.price = product.price
        if product.expiry:
            existing_product.expiry = product.expiry
        if product.brand:
            existing_product.brand = product.brand
        if product.weight:
            existing_product.weight = product.weight
        if product.category_id:
            existing_product.category_id = product.category_id
        if product.sku:
            existing_product.sku = product.sku
        if product.stock_quantity:
            existing_product.stock_quantity = product.stock_quantity
        if product.reorder_level:
            existing_product.reorder_level = product.reorder_level
        if product.meta_title:
            existing_product.meta_title = product.meta_title
        if product.meta_description:
            existing_product.meta_description = product.meta_description
        if product.meta_keywords:
            existing_product.meta_keywords = product.meta_keywords
        
        existing_product.updated_at = datetime.now()
        
        # Commit the updates to the database
        db.commit()
        db.refresh(existing_product)
        logger.info(f"Product updated: {existing_product}")
        return existing_product
    else:
        logger.warning(f"Product not found with id: {product_id}")
        return None


# Delete product from database
def delete_product_from_db(product_id: int, db: Session):
    # Fetch the existing product from the database
    existing_product = db.exec(select(Product).where(Product.id == product_id)).first()
    
    if existing_product:
        # Delete the product
        db.delete(existing_product)
        db.commit()
        logger.info(f"Product deleted: {existing_product}")
    else:
        logger.warning(f"Product not found with id: {product_id}")
