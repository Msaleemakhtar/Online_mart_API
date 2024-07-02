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
    id:UUID | None = Field(default_factory=uuid4, primary_key=True, index=True)
    order_id:UUID | None = Field(foreign_key="order.id", index=True)
    product_id: int
    product_price: float
    quantity: int
    total_price: float
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    order: "Order" = Relationship(back_populates="items")


class Order(SQLModel, table=True):
    id:UUID | None = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: str
    total_price: float = 0.0
    items_count: int = 0  # Added to keep track of total items
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    items: List[OrderItem] = Relationship(back_populates="order")

class OrderItemCreate(SQLModel):
    product_id: int
    product_price: float
    quantity: int
    total_price: float

class OrderCreate(SQLModel):
    user_id: str
    items: List[OrderItemCreate]

class OrderUpdate(SQLModel):
    user_id: Optional[str] = None
    items: Optional[List[OrderItemCreate]] = None
    status: Optional[OrderStatus] = None

    
    

# Inventory schema

class InventoryItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int 
    stock_quantity: int
    reorder_level: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )



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





