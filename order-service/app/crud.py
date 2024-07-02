from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, select
from aiokafka import AIOKafkaProducer
from uuid import uuid4, UUID
from app.models.order_model import OrderItem, Order, InventoryItem, User, OrderCreate, OrderStatus
from app import settings, order_pb2

# Get All inventory from the Database
async def get_inventory(session: Session):
    all_products = session.exec(select(InventoryItem)).all()
    return all_products

# Get All users from the Database
async def get_users(session: Session):
    all_users = session.exec(select(User)).all()
    return all_users

#get all orders
async def get_orders(session: Session):
    all_orders = session.exec(select(Order)).all()
    return all_orders

# Create Order and send to kafka
async def create_order(order_create:OrderCreate, db: Session, producer:AIOKafkaProducer):
    # Check if the user exists
    user = db.exec(select(User).where(User.id == order_create.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
     
    total_price = 0
    total_items = 0
    for item in order_create.items:
        # Check if the product exists
        product = db.exec(select(InventoryItem).where(InventoryItem.id == item.product_id)).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
       
        #Calculate the total price and total items
        item.total_price = item.product_price * item.quantity
        total_price += item.total_price
        total_items += item.quantity
        
    # Create the order 
    order = Order(
        user_id=order_create.user_id,
        total_price=total_price,
        items_count=total_items,
        status= OrderStatus.PENDING
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    
    # Create order items
    order_items = []
    for item in order_create.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_price=item.product_price,
            total_price=item.total_price
        )
        db.add(order_item)
        order_items.append(order_item)
        
    db.commit()
    # Refresh order items to get IDs
    for order_item in order_items:
        db.refresh(order_item)
    order.items = order_items
    
    
    # Prepare protobuf message
    order_message = order_pb2.OrderOperation(
        operation=order_pb2.OperationType.CREATE,
        order=order_pb2.Order(
            id= str(order.id),
            user_id=order.user_id,
            total_price=float(order.total_price),
            items_count=order.items_count,
            status=order_pb2.OrderStatus.PENDING,
            items=[
                order_pb2.OrderItem(
                    id=str(item.id),
                    order_id=str(order.id),
                    product_id=int(item.product_id),
                    quantity=int(item.quantity),
                    product_price=float(item.product_price),
                    total_price=float(item.total_price),
                ) for item in order_items
            ])
    )

    # Serialize the protobuf message
    order_message_serialized = order_message.SerializeToString()

    # Send protobuf message to Kafka
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_message_serialized)

    return order
    


# Delete Order and send to Kafka

async def delete_order(order_id:UUID, db: Session, producer: AIOKafkaProducer):
    # Fetch the existing order
    
   
    order = db.exec(select(Order).where(Order.id == order_id)).first()
    
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
 
    # Prepare protobuf message before deleting the order
    order_message = order_pb2.OrderOperation(
        operation=order_pb2.OperationType.DELETE,
        order=order_pb2.Order(
            id=str(order.id),
            user_id=str(order.user_id),
            total_price=float(order.total_price),
            items_count=order.items_count,
            status=order_pb2.OrderStatus.CANCELED,
            )
    )

    # Serialize the protobuf message
    order_message_serialized = order_message.SerializeToString()

    # Send protobuf message to Kafka
    await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_message_serialized)

    # Fetch and delete the order items
    order_items = db.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()
    for item in order_items:
        db.delete(item)
    
    # Delete the order itself
    db.delete(order)
    db.commit()

    return {"detail": "Order deleted successfully"}