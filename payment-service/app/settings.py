from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()
    
STRIPE_SECRET_KEY= config("STRIPE_SECRET_KEY", cast=str)
STRIPE_WEBHOOK_SECRET= config("STRIPE_WEBHOOK_SECRET", cast= str)

DATABASE_URL = config("DATABASE_URL", cast=str)
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT", cast=str)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=str)
