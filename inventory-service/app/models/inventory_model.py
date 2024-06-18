from sqlmodel import SQLModel, Field
from datetime import datetime

class InventoryItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int 
    stock_quantity: int
    reorder_level: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )

# The Product table can be referenced from the Product microservice, 
# it does not need to be duplicated if you're only referencing product_id.
