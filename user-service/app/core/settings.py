from starlette.config import Config
from starlette.datastructures import Secret


try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()



DATABASE_URL = config("DATABASE_URL", cast=str, )

# BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
# KAFKA_USER_TOPIC = config("KAFKA_USER_TOPIC", cast=str)
# KAFKA_CONSUMER_GROUP_ID_FOR_USER = config("KAFKA_CONSUMER_GROUP_ID_FOR_USER", cast=str)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=str)

SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALGORITHM = config("ALGORITHM", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=Secret)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=Secret)