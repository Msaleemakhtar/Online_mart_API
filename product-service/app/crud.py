from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.product_model import Product, ProductRating, ProductRatingCreate
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


# Serach and filter product by id, name, category_id , max_price, min_price, brand
def get_filtered_products(
    session: Session,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    brand: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    stmt = select(Product)
    
   
    if name:
        stmt = stmt.where(Product.name.contains(name))
    if category_id:
        stmt = stmt.where(Product.category_id == category_id)
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)
    if brand:
        stmt = stmt.where(Product.brand == brand)
    
    stmt = stmt.offset(skip).limit(limit)
    products = session.exec(stmt).all()
    
    # # Fetch ratings for each product
    # for product in products:
    #     product.ratings = session.exec(select(ProductRating).where(ProductRating.product_id == product.id)).all()
    
    return products



# Get product rating
def get_ratings_for_product(session: Session, product_id: int) -> list[ProductRating]:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    ratings = session.exec(select(ProductRating).where(ProductRating.product_id == product_id)).all()
    return ratings

# Create the raing of product
def create_product_rating(session: Session, product_id: int, rating: ProductRatingCreate) -> ProductRating:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_rating = ProductRating(product_id=product_id, **rating.dict())
    session.add(product_rating)
    session.commit()
    session.refresh(product_rating)
    return product_rating


# def update_product_rating(session: Session, rating_id: int, rating_data: ProductRatingCreate) -> ProductRating:
#     rating = session.get(ProductRating, rating_id)
#     if not rating:
#         raise HTTPException(status_code=404, detail="Rating not found")
    
#     for field, value in rating_data.dict(exclude_unset=True).items():
#         setattr(rating, field, value)
    
#     session.add(rating)
#     session.commit()
#     session.refresh(rating)
#     return rating



# Update the rating 
def update_product_rating(session: Session, rating_id: int, rating_data: ProductRatingCreate) -> ProductRating:
    rating = session.get(ProductRating, rating_id)
    if rating:
        rating.rating = rating_data.rating
        rating.review = rating_data.review
        rating.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(rating)
    return rating


# Get the average rating
def get_average_rating(session: Session, product_id: int) -> float:
    statement = select(ProductRating.rating).where(ProductRating.product_id == product_id)
    ratings = session.exec(statement).all()
    if not ratings:
        return 0.0
    return sum(ratings) / len(ratings)
