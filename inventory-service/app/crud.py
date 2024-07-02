from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItem
from app.inventory_pb2 import InventoryItem as InventoryItemProto


def convert_inventory_item_to_proto(inventory_item: InventoryItem) -> InventoryItemProto:
    return InventoryItemProto(
        id=inventory_item.id,
        product_id=inventory_item.product_id,
        stock_quantity=inventory_item.stock_quantity,
        reorder_level=inventory_item.reorder_level,
        created_at=inventory_item.created_at.isoformat(),
        updated_at=inventory_item.updated_at.isoformat() if inventory_item.updated_at else ""
    )
    
    
# Get All Inventory from the Database
def get_all_inventory_items(session: Session):
    all_inventory = session.exec(select(InventoryItem)).all()
    return all_inventory

# Get Inventory by productID from Database
def get_inventory_by_id(product_id: int, session: Session):
    product = session.exec(select(InventoryItem).where(InventoryItem.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
