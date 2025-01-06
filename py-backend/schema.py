from pydantic import BaseModel

class StockBase(BaseModel):
    value: str
    name: str

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    class Config:
        orm_mode = True