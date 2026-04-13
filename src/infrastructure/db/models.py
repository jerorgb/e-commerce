from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, DateTime

from src.infrastructure.db.database import Base


class ProductModel(Base):
    """Modelo ORM que representa la tabla de productos."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    size = Column(String(20), nullable=True)
    color = Column(String(50), nullable=True)
    price = Column(Float, nullable=True)
    stock = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)


class ChatMemoryModel(Base):
    """Modelo ORM que representa la tabla de historial de chat."""

    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), index=True, nullable=False)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
