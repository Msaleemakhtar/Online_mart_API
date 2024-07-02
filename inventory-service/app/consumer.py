from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app.product_pb2 import Product, OperationType as ProductOperationType
from app.inventory_pb2 import InventoryOperation, OperationType as InventoryOperationType,InventoryItem as InventoryItemProto
from app.crud import convert_inventory_item_to_proto
from app.models.inventory_model import InventoryItem
from app.producer import get_kafka_producer
from sqlmodel import Session, select
from app.db import get_session
from datetime import datetime
from app import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_PRODUCT_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
        auto_offset_reset='latest'
    )
    producer = AIOKafkaProducer(bootstrap_servers=settings.BOOTSTRAP_SERVER)
    await producer.start()
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                product = Product()
                product.ParseFromString(msg.value)
                logger.info(f"Received product: {product}")
                with next(get_session()) as session:
                    if product.operation == ProductOperationType.CREATE:
                        new_inventory = InventoryItem(
                            product_id=product.id,
                            stock_quantity=product.stock_quantity,
                            reorder_level=product.reorder_level,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        session.add(new_inventory)
                        session.commit()
                        logger.info(f"Inventory created: {new_inventory}")

                        # Produce inventory operation to Kafka
                        inventory_operation = InventoryOperation(
                            operation=InventoryOperationType.CREATE,
                            inventory_item=convert_inventory_item_to_proto(new_inventory)
                        )
                        await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, inventory_operation.SerializeToString())

                    elif product.operation == ProductOperationType.UPDATE:
                        product_id = product.id
                        existing_inventory = session.exec(select(InventoryItem).where(InventoryItem.id == product_id)).first()
                        if existing_inventory:
                            if product.stock_quantity:
                                existing_inventory.stock_quantity = product.stock_quantity
                            if product.reorder_level:
                                existing_inventory.reorder_level = product.reorder_level
                            existing_inventory.updated_at = datetime.now()
                            session.commit()
                            logger.info(f"Inventory updated: {existing_inventory}")

                            # Produce inventory operation to Kafka
                            inventory_operation = InventoryOperation(
                                operation=InventoryOperationType.UPDATE,
                                inventory_item=convert_inventory_item_to_proto(existing_inventory)
                            )
                            await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, inventory_operation.SerializeToString())
                        else:
                            logger.warning(f"Inventory not found with id: {product_id}")

                    elif product.operation == ProductOperationType.DELETE:
                        product_id = product.id
                        existing_inventory = session.exec(select(InventoryItem).where(InventoryItem.id == product_id)).first()
                        if existing_inventory:
                            session.delete(existing_inventory)
                            session.commit()
                            logger.info(f"Inventory deleted: {existing_inventory}")

                            # Produce inventory operation to Kafka
                            inventory_operation = InventoryOperation(
                                operation=InventoryOperationType.DELETE,
                                inventory_item=convert_inventory_item_to_proto(existing_inventory)
                            )
                            await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, inventory_operation.SerializeToString())
                        else:
                            logger.warning(f"Inventory not found with id: {product_id}")

                    else:
                        logger.warning(f"Unknown operation type: {product.operation}")

            except Exception as e:
                logger.exception("Error processing message: %s", e)

    except Exception as e:
        logger.exception("Error in consumer loop: %s", e)

    finally:
        await consumer.stop()
        await producer.stop()






































# from datetime import datetime
# import logging
# from app import product_pb2
# from aiokafka import AIOKafkaConsumer
# #from aiokafka.errors import KafkaConnectionError, KafkaError

# from app import settings
# from app.db import engine, Session, get_session
# from app.models.inventory_model import InventoryItem 
# from sqlmodel import select

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# async def consume():
#     consumer = AIOKafkaConsumer(
#         settings.KAFKA_PRODUCT_TOPIC,
#         bootstrap_servers=settings.BOOTSTRAP_SERVER,
#         group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
#         auto_offset_reset='latest'
#     )
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             try:
#                 product = product_pb2.Product()
#                 product.ParseFromString(msg.value)
#                 logger.info(f"Received product: {product}")
#                 with next(get_session()) as session:

#                     if product.operation == product_pb2.OperationType.CREATE:
#                         new_inventory = InventoryItem( 
#                             product_id=product.id,                   
#                             stock_quantity=product.stock_quantity,
#                             reorder_level=product.reorder_level,
#                             created_at=datetime.now(),
#                             updated_at=datetime.now()
#                         )
#                         logger.info(f"new inventory : {new_inventory}")
#                         session.add(new_inventory)
#                         session.commit()
#                         logger.info(f"inventory created: {new_inventory}")

#                     elif product.operation == product_pb2.OperationType.UPDATE:
#                         product_id = product.id
#                         existing_invenory = session.exec(select(InventoryItem).where(InventoryItem.id == product_id)).first()
#                         if existing_invenory:
#                             # Update only the fields that are present in the protobuf message
#                             if product.stock_quantity:
#                                 existing_invenory.stock_quantity = product.stock_quantity
#                             if product.reorder_level:
#                                 existing_invenory.reorder_level = product.reorder_level     
#                             existing_invenory.updated_at = datetime.now()
#                             session.commit()
#                             logger.info(f"Inventory updated: {existing_invenory}")
#                         else:
#                             logger.warning(f"Inventory not found with id: {existing_invenory}")


#                     elif product.operation == product_pb2.OperationType.DELETE:
#                         product_id = product.id
#                         existing_invenory = session.exec(select(InventoryItem).where(InventoryItem.id == product_id)).first()
#                         if existing_invenory:
#                             session.delete(existing_invenory)
#                             session.commit()
#                             logger.info(f"Inventory deleted: {existing_invenory}")
#                         else:
#                             logger.warning(f"Inventory not found with id: {existing_invenory}")

#                     else:
#                         logger.warning(f"Unknown operation type: {product.operation}")

#             except Exception as e:
#                 logger.exception("Error processing message: %s", e)

#     except Exception as e:
#         logger.exception("Error in consumer loop: %s", e)

#     finally:
#         try:
#             await consumer.stop()
#         except Exception as e:
#             logger.exception("Error stopping consumer: %s", e)
