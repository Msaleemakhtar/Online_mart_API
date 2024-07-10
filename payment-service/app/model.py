from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    PAID = "PAID"

class Payment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID
    total_price: float
    currency: str
    user_email: str
    checkout_session_id: str
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    

class PaymentRequest(SQLModel):
    order_id: UUID
    total_price: int
    user_email: str
    currency: str


class PaymentResponse(PaymentRequest):
    id: int
    