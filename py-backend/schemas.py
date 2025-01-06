from pydantic import BaseModel

class StockBase(BaseModel):
    value: str
    name: str

    class Config:
        from_attributes = True


class CreateStock(StockBase):
    class Config:
        from_attributes = True