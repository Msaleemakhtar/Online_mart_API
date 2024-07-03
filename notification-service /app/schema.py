from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, Union
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    USER_CREATED = "USER_CREATED"
    ORDER_CREATED = "ORDER_CREATED"
    ORDER_UPDATED = "ORDER_UPDATED"
    ORDER_DELETED = "ORDER_DELETED"

class Notification(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    recipient: str
    subject: str
    body: str
    sent_at: datetime = Field(default_factory=datetime.now)
    notification_type: NotificationType

class NotificationBase(SQLModel):
    recipient: str
    subject: str
    body: str
    notification_type: NotificationType

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: UUID
    sent_at: datetime

    class Config:
        orm_mode = True
