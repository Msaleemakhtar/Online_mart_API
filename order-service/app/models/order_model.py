from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, Union
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum





class OrderStatus(str, Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELED = "canceled"




class OrderItem(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    order_id: Optional[UUID] = Field(foreign_key="order.id", index=True)
    product_id: str
    quantity: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    order: "Order" = Relationship(back_populates="items")



class Order(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: str
    total_price: float = 0.0
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    items: List[OrderItem] = Relationship(back_populates="order")


class OrderItemCreate(SQLModel):
    product_id: str
    quantity: int

class OrderCreate(SQLModel):
    user_id: str
    total_price: float = 0.0
    items: List[OrderItemCreate]

class OrderUpdate(SQLModel):
    id: UUID
    user_id: Optional[str] = None
    items: Optional[List[OrderItemCreate]] = None
    status: Optional[OrderStatus] = None
    
    
    

# product schema

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    expiry: str | None = None
    brand: str | None = None
    weight: float | None = None
    sku: str | None = None
    stock_quantity: int | None = None
    reorder_level: int | None = None
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    

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



# user schema


class User(SQLModel, table=True):
    """
    Represents a generic user model with fields for ID, hashed password, email verification status,
    and timestamps for creation and update.
    """
    id:UUID | None = Field(default_factory=uuid4, primary_key=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name:str = Field()
    email: str = Field(unique=True, index=True)
    email_verified: Union[bool, None] = None
    updated_at: datetime | None = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    created_at: datetime = Field(default_factory=datetime.now)





