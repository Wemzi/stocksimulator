from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status
import model
import schemas
from db import get_db

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)

@router.get('/', response_model=List[schemas.Stock])
async def get_stocks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock))
    stocks = result.scalars().all()
    return stocks

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Stock)
async def create_stock(stock: schemas.StockCreate, db: AsyncSession = Depends(get_db)):
    new_stock = model.Stock(**stock.dict())
    db.add(new_stock)
    await db.commit()
    await db.refresh(new_stock)
    return new_stock

@router.get('/{id}', response_model=schemas.Stock, status_code=status.HTTP_200_OK)
async def get_stock(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock).filter(model.Stock.id == id))
    stock = result.scalar_one_or_none()
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} you requested does not exist")
    return stock

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock).filter(model.Stock.id == id))
    stock = result.scalar_one_or_none()
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} you requested does not exist")
    await db.delete(stock)
    await db.commit()

@router.put('/{id}', response_model=schemas.Stock)
async def update_stock(id: int, stock_update: schemas.StockUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock).filter(model.Stock.id == id))
    stock = result.scalar_one_or_none()
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")
    for key, value in stock_update.dict().items():
        setattr(stock, key, value)
    await db.commit()
    await db.refresh(stock)
    return stock

@router.post('/{id}/value', response_model=schemas.StockValue)
async def create_stock_value(id: int, stock_value: schemas.StockValueCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock).filter(model.Stock.id == id))
    stock = result.scalar_one_or_none()
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")
    new_value = model.StockValue(stock_id=id, **stock_value.dict())
    db.add(new_value)
    await db.commit()
    await db.refresh(new_value)
    
    # Calculate the percentage change
    previous_value = await db.execute(select(model.StockValue).filter(model.StockValue.stock_id == id).order_by(model.StockValue.timestamp.desc()))
    previous_value = previous_value.scalars().first()
    if previous_value:
        percentage_change = ((new_value.value - previous_value.value) / previous_value.value) * 100
        stock.percentage_change = percentage_change
    
    # Update the latest value and low_w/high_w fields if necessary
    stock.latest_value = new_value.value
    if new_value.value < stock.low_w:
        stock.low_w = new_value.value
    if new_value.value > stock.high_w:
        stock.high_w = new_value.value
    await db.commit()
    await db.refresh(stock)

    return new_value

@router.get('/{id}/values', response_model=List[schemas.StockValue])
async def get_stock_values(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.StockValue).filter(model.StockValue.stock_id == id))
    values = result.scalars().all()
    if not values:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No values found for stock id: {id}")
    return values
