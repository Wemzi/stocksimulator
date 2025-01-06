from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import model
import schema
from fastapi import APIRouter
from db import get_db

router = APIRouter(
    prefix='/stocks',
    tags=['stocks']
)

@router.get('/', response_model=List[schemas.Createstock])
def test_stocks(db: Session = Depends(get_db)):

    stock = db.query(models.stock).all()


    return  stock

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.Createstock])
def test_stocks_sent(stock_stock:schemas.Createstock, db:Session = Depends(get_db)):

    new_stock = models.stock(**stock_stock.dict())
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return [new_stock]


@router.get('/{id}', response_model=schemas.Createstock, status_code=status.HTTP_200_OK)
def get_test_one_stock(id:int ,db:Session = Depends(get_db)):

    idv_stock = db.query(models.stock).filter(models.stock.id == id).first()

    if idv_stock is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return idv_stock

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test_stock(id:int, db:Session = Depends(get_db)):

    deleted_stock = db.query(models.stock).filter(models.stock.id == id)


    if deleted_stock.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_stock.delete(synchronize_session=False)
    db.commit()



@router.put('/stocks/{id}', response_model=schemas.Createstock)
def update_test_stock(update_stock:schemas.stockBase, id:int, db:Session = Depends(get_db)):

    updated_stock =  db.query(models.stock).filter(models.stock.id == id)

    if updated_stock.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_stock.update(update_stock.dict(), synchronize_session=False)
    db.commit()


    return  updated_stock.first()