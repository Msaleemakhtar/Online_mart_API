from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItem



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
