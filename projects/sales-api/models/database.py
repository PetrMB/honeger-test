"""Sales API models."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Date, DECIMAL, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Products table (normalized names)
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    normalized_name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), index=True)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")

    __table_args__ = (
        Index("idx_normalized", "normalized_name"),
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}')>"

# Shops table
class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True)
    slug = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    logo_url = Column(Text)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")

    def __repr__(self):
        return f"<Shop(id={self.id}, slug='{self.slug}', name='{self.name}')>"

# Sales table (active deals)
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    shop_id = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))
    price_text = Column(String(50))
    original_price = Column(DECIMAL(10, 2))
    discount_percent = Column(Integer)
    valid_from = Column(Date)
    valid_until = Column(Date)
    validity_text = Column(String(100))
    source_url = Column(Text)
    scraped_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")

    __table_args__ = (
        Index("idx_product_shop", "product_id", "shop_id"),
        Index("idx_valid_dates", "valid_from", "valid_until"),
    )

    def __repr__(self):
        return f"<Sale(id={self.id}, product_id={self.product_id}, shop_id={self.shop_id}, price={self.price})>"

# Price history table
class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    shop_id = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2))
    recorded_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")

    __table_args__ = (
        Index("idx_product_time", "product_id", "recorded_at"),
    )

    def __repr__(self):
        return f"<PriceHistory(id={self.id}, product_id={self.product_id}, price={self.price})>"
