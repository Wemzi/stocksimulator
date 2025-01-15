from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, nullable=False)
    stock_name = Column(String, nullable=False)
    value = Column(Integer, nullable=True)
    high_w = Column(Integer, nullable=True )
    low_w = Column(Integer, nullable=True)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
