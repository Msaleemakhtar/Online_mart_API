from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=str)
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)

KAFKA_USER_TOPIC = config("KAFKA_USER_TOPIC", cast=str)
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION = config("KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION", cast=str)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=str)