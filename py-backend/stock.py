from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status
import model
import schemas
import stock
from fastapi import APIRouter
from db import get_db

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)

@router.get('/', response_model=List[schemas.CreateStock])
async def test_stocks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock))
    stocks = result.scalars().all()
    return stocks

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateStock)
async def test_stocks_sent(stock_stock: schemas.CreateStock, db: AsyncSession = Depends(get_db)):
    new_stock = model.Stock(**stock_stock.dict())
    db.add(new_stock)
    await db.commit()
    await db.refresh(new_stock)
    return new_stock

@router.get('/{id}', response_model=schemas.CreateStock, status_code=status.HTTP_200_OK)
async def get_test_one_stock(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock).filter(model.Stock.id == id))
    idv_stock = result.scalar_one_or_none()
    if idv_stock is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return idv_stock

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_stock(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock).filter(model.Stock.id == id))
    deleted_stock = result.scalar_one_or_none()
    if deleted_stock is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    await db.delete(deleted_stock)
    await db.commit()

@router.put('/stocks/{id}', response_model=schemas.CreateStock)
async def update_test_stock(update_stock: schemas.StockBase, id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Stock).filter(model.Stock.id == id))
    updated_stock = result.scalar_one_or_none()
    if updated_stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")
    for key, value in update_stock.dict().items():
        setattr(updated_stock, key, value)
    await db.commit()
    await db.refresh(updated_stock)
    return updated_stock
