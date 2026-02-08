"""Price history model"""
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", backref="price_history")
    shop = relationship("Shop", backref="price_history")
    
    __table_args__ = (
        Index('idx_product_time', 'product_id', 'recorded_at'),
    )
    
    def __repr__(self):
        return f"<PriceHistory {self.product.name} - {self.price}>"
