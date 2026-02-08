"""Sale model"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    
    price = Column(Numeric(10, 2), nullable=True)
    price_text = Column(String(50), nullable=True)
    original_price = Column(Numeric(10, 2), nullable=True)
    discount_percent = Column(Integer, nullable=True)
    
    valid_from = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=True)
    validity_text = Column(String(100), nullable=True)
    
    source_url = Column(String(255), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", backref="sales")
    shop = relationship("Shop", backref="sales")
    
    __table_args__ = (
        Index('idx_product_shop', 'product_id', 'shop_id'),
        Index('idx_valid_dates', 'valid_from', 'valid_until'),
    )
    
    def __repr__(self):
        return f"<Sale {self.product.name} @ {self.shop.name} - {self.price_text}>"
