from datetime import datetime
import logging
from aiokafka import AIOKafkaConsumer
from sqlmodel import select
from app import settings
from app.db import get_session
from app.models.order_model import User
from uuid import UUID
from app import user_pb2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def user_consume():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_USER_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        auto_offset_reset='latest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                user_operation = user_pb2.UserOperation()
                user_operation.ParseFromString(msg.value)
                user = user_operation.user
                logger.info(f"Received user: {user}")

                # Extract and validate UUID
                user_id_str = user.id  # Assuming user.id is a string representation of UUID
                try:
                    user_id = UUID(user_id_str)
                except ValueError:
                    logger.error(f"Invalid UUID format for user ID: {user_id_str}")
                    continue

                with next(get_session()) as session:
                    # Check if user already exists
                    existing_user = session.exec(select(User).where(User.id == user_id)).first()
                    if existing_user:
                        logger.info(f"User already exists: {existing_user}")
                        continue  # Skip the rest of the loop for this message

                    # Create new user
                    new_user = User(
                        id=user_id,
                        username=user.username,
                        full_name=user.full_name,
                        email=user.email,
                        email_verified=user.email_verified,
                        updated_at=datetime.now(),
                        created_at=datetime.now()
                    )
                    logger.info(f"New user: {new_user}")
                    session.add(new_user)
                    session.commit()
                    logger.info(f"User created: {new_user}")

            except Exception as e:
                logger.exception("Error processing message: %s", e)

    except Exception as e:
        logger.exception("Error in consumer loop: %s", e)

    finally:
        try:
            await consumer.stop()
        except Exception as e:
            logger.exception("Error stopping consumer: %s", e)
