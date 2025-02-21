from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, nullable=False)
    stock_name = Column(String, nullable=False)
    high_w = Column(Integer, nullable=True)
    low_w = Column(Integer, nullable=True)
    percentage_change = Column(Float, nullable=True)
    latest_value = Column(Integer, nullable=True)

    values = relationship("StockValue", back_populates="stock", cascade="all, delete")

class StockValue(Base):
    __tablename__ = "stock_values"

    id = Column(Integer, primary_key=True, nullable=False)
    stock_id = Column(Integer, ForeignKey('stocks.id', ondelete="CASCADE"), nullable=False)
    value = Column(Integer, nullable=True)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    stock = relationship("Stock", back_populates="values")