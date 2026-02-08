"""Product model"""
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from .base import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    normalized_name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_normalized_name', 'normalized_name'),
    )
    
    def __repr__(self):
        return f"<Product {self.name}>"
