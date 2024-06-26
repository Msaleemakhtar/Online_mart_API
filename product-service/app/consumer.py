from datetime import datetime
import logging
from app import product_pb2
from aiokafka import AIOKafkaConsumer
#from aiokafka.errors import KafkaConnectionError, KafkaError

from app import settings
from app.db import get_session
from app.models.product_model import Product, Category
from sqlmodel import select

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_PRODUCT_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT,
        auto_offset_reset='latest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                product = product_pb2.Product()
                product.ParseFromString(msg.value)
                logger.info(f"Received product: {product}")
                with next(get_session()) as session:
                    # Check if the category exists, if not, create it
                    category = session.exec(select(Category).where(Category.id == product.category_id)).first()
                    if not category:
                        new_category = Category(id=product.category_id, name=f"Category {product.category_id}")
                        session.add(new_category)
                        session.commit()
                        logger.info(f"Category created: {new_category}")

                    if product.operation == product_pb2.OperationType.CREATE:
                        new_product = Product(
                            name=product.name,
                            description=product.description,
                            price=product.price,
                            expiry=product.expiry,
                            brand=product.brand,
                            weight=product.weight,
                            category_id=product.category_id,
                            sku=product.sku,
                            stock_quantity=product.stock_quantity,
                            reorder_level=product.reorder_level,
                            meta_title=product.meta_title,
                            meta_description=product.meta_description,
                            meta_keywords=product.meta_keywords,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        logger.info(f"new product: {new_product}")
                        session.add(new_product)
                        session.commit()
                        logger.info(f"Product created: {new_product}")

                    elif product.operation == product_pb2.OperationType.UPDATE:
                        product_id = product.id
                        existing_product = session.exec(select(Product).where(Product.id == product_id)).first()
                        if existing_product:
                            # Update only the fields that are present in the protobuf message
                            if product.name:
                                existing_product.name = product.name
                            if product.description:
                                existing_product.description = product.description
                            if product.price:
                                existing_product.price = product.price
                            if product.expiry:
                                existing_product.expiry = product.expiry
                            if product.brand:
                                existing_product.brand = product.brand
                            if product.weight:
                                existing_product.weight = product.weight
                            if product.category_id:
                                existing_product.category_id = product.category_id
                            if product.sku:
                                existing_product.sku = product.sku
                            if product.stock_quantity:
                                existing_product.stock_quantity = product.stock_quantity
                            if product.reorder_level:
                                existing_product.reorder_level = product.reorder_level
                            if product.meta_title:
                                existing_product.meta_title = product.meta_title
                            if product.meta_description:
                                existing_product.meta_description = product.meta_description
                            if product.meta_keywords:
                                existing_product.meta_keywords = product.meta_keywords
                                
                            existing_product.updated_at = datetime.utcnow()
                            session.commit()
                            logger.info(f"Product updated: {existing_product}")
                        else:
                            logger.warning(f"Product not found with id: {product_id}")


                    elif product.operation == product_pb2.OperationType.DELETE:
                        product_id = product.id
                        existing_product = session.exec(select(Product).where(Product.id == product_id)).first()
                        if existing_product:
                            session.delete(existing_product)
                            session.commit()
                            logger.info(f"Product deleted: {existing_product}")
                        else:
                            logger.warning(f"Product not found with id: {product_id}")

                    else:
                        logger.warning(f"Unknown operation type: {product.operation}")

            except Exception as e:
                logger.exception("Error processing message: %s", e)

    except Exception as e:
        logger.exception("Error in consumer loop: %s", e)

    finally:
        try:
            await consumer.stop()
        except Exception as e:
            logger.exception("Error stopping consumer: %s", e)
