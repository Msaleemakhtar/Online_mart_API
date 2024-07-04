from sqlmodel import SQLModel, create_engine, Session
from app.models.order_model import OrderItem, Order
from app import settings



connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

    
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
 
 
 
    
def get_session():
    with Session(engine) as session:
        yield session