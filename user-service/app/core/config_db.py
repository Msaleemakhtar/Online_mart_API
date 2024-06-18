from sqlmodel import SQLModel,Session, create_engine
from app.core import settings
from app.models import User


connection_str = str(settings.DB_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_str, connect_args={"sslmode": "require"}, pool_recycle= 300)


def get_db():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)