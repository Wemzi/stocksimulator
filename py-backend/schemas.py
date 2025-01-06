from pydantic import BaseModel

class StockBase(BaseModel):
    stock_name: str
    value: int
    high_w: int
    low_w: int

    class Config:
        from_attributes = True
        
class CreateStock(StockBase):
    id: int
    
    class Config:
        from_attributes = True