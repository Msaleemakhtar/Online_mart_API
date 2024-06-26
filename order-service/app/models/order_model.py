from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
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