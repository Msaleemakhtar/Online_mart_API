from datetime import datetime
import logging
from app import inventory_pb2
from aiokafka import AIOKafkaConsumer
from sqlmodel import select

from app import settings
from app.db import get_session
from app.models.order_model import InventoryItem  # Adjust based on your actual model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def inventory_consume():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_INVENTORY_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        auto_offset_reset='latest'
    )
    await consumer.start()
    
    try:
        async for msg in consumer:
            try:
                inventory_operation = inventory_pb2.InventoryOperation()
                inventory_operation.ParseFromString(msg.value)
                logger.info(f"Received inventory operation: {inventory_operation}")
                
                inventory_item = inventory_operation.inventory_item
                operation_type = inventory_operation.operation

                with next(get_session()) as session:
                    if operation_type == inventory_pb2.OperationType.CREATE:
                        new_inventory_item = InventoryItem(
                            id=inventory_item.id,
                            product_id=inventory_item.product_id,
                            stock_quantity=inventory_item.stock_quantity,
                            reorder_level=inventory_item.reorder_level,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        session.add(new_inventory_item)
                        session.commit()
                        logger.info(f"Inventory item created: {new_inventory_item}")

                    elif operation_type == inventory_pb2.OperationType.UPDATE:
                        existing_inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item.id)).first()
                        if existing_inventory_item:
                            # Update only the fields that are present in the protobuf message
                            if inventory_item.product_id:
                                existing_inventory_item.product_id = inventory_item.product_id
                            if inventory_item.stock_quantity:
                                existing_inventory_item.stock_quantity = inventory_item.stock_quantity
                            if inventory_item.reorder_level:
                                existing_inventory_item.reorder_level = inventory_item.reorder_level
                                
                            existing_inventory_item.updated_at = datetime.utcnow()
                            session.commit()
                            logger.info(f"Inventory item updated: {existing_inventory_item}")
                        else:
                            logger.warning(f"Inventory item not found with id: {inventory_item.id}")

                    elif operation_type == inventory_pb2.OperationType.DELETE:
                        existing_inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item.id)).first()
                        if existing_inventory_item:
                            session.delete(existing_inventory_item)
                            session.commit()
                            logger.info(f"Inventory item deleted: {existing_inventory_item}")
                        else:
                            logger.warning(f"Inventory item not found with id: {inventory_item.id}")

                    else:
                        logger.warning(f"Unknown operation type: {operation_type}")

            except Exception as e:
                logger.exception("Error processing message: %s", e)

    except Exception as e:
        logger.exception("Error in consumer loop: %s", e)

    finally:
        try:
            await consumer.stop()
        except Exception as e:
            logger.exception("Error stopping consumer: %s", e)
