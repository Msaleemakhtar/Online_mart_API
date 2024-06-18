from typing import List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    products: List["Product"] = Relationship(back_populates="category")

class ProductImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    url: str
    alt_text: str | None = None
    product: "Product" = Relationship(back_populates="images")

class ProductTagLink(SQLModel, table=True):
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    products: List["Product"] = Relationship(back_populates="tags", link_model=ProductTagLink)

class ProductRating(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    rating: int
    review: str | None = None
    product: "Product" = Relationship(back_populates="ratings")
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    expiry: str | None = None
    brand: str | None = None
    weight: float | None = None
    category_id: int | None = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
    sku: str | None = None
    stock_quantity: int | None = None
    reorder_level: int | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    images: List[ProductImage] = Relationship(back_populates="product")
    ratings: List[ProductRating] = Relationship(back_populates="product")
    tags: List[Tag] = Relationship(back_populates="products", link_model=ProductTagLink) 
    

class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    expiry: str | None = None
    brand: str | None = None
    weight: float | None = None
    category_id: int | None = None
    sku: str | None = None
    stock_quantity: int | None = None
    reorder_level: int | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: str | None = None




class ProductRatingCreate(SQLModel):
    rating: float = Field(gt=0, le=5)  # Rating should be a decimal number between 0 and 5
    review: str = Field(default=None, nullable=True)  # Optional review text