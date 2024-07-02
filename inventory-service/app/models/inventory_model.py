from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional




class InventoryItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int 
    stock_quantity: int
    reorder_level: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )


class StockAdjustment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    inventory_item_id: int = Field(default=None, foreign_key="inventoryitem.id")
    adjustment_type: str
    quantity: int
    reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    inventory_item: InventoryItem = Relationship()