from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer,primary_key=True,nullable=False)
    stock_name = Column(String,nullable=False)
    value = Column(Integer,nullable=False)
    high_w = Column(Integer,nullable=False)
    low_w = Column(Boolean, server_default='TRUE')
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text('now()'))