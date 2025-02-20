from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StockBase(BaseModel):
    stock_name: str
    high_w: int
    low_w: int

    class Config:
        from_attributes = True

class StockCreate(StockBase):
    id: int

    class Config:
        from_attributes = True

class StockValueBase(BaseModel):
    stock_id: int
    value: int
    timestamp: datetime

    class Config:
        from_attributes = True

class CreateStockValue(StockValueBase):
    id: int

    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    stock_name: Optional[str]
    high_w: Optional[int]
    low_w: Optional[int]

    class Config:
        from_attributes = True

class Stock(BaseModel):
    id: int
    stock_name: str
    high_w: int
    low_w: int

    class Config:
        from_attributes = True

class StockValue(BaseModel):
    id: int
    stock_id: int
    value: int
    timestamp: datetime

    class Config:
        from_attributes = True

class StockValueCreate(StockValueBase):
    pass
