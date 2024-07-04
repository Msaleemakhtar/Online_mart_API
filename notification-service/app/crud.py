from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, select
from aiokafka import AIOKafkaProducer
from uuid import uuid4, UUID
from app.schema import OrderItem
from app import settings, order_pb2

