from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime, timedelta
from model import Stock
import schemas
import stock
from db import engine, create_tables, get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging
import asyncio

last_run_time = datetime.now()
app = FastAPI()
app.include_router(stock.router)

stocks = [
    {"stock_name": "AAPL", "value": 150.00, "change_24h": 1.5, "high_w": 155, "low_w": 145},
    {"stock_name": "MSFT", "value": 250.00, "change_24h": -0.8, "high_w": 260, "low_w": 240},
    {"stock_name": "GOOGL", "value": 2800.00, "change_24h": 2.1, "high_w": 2850, "low_w": 2750},
    {"stock_name": "AMZN", "value": 3400.00, "change_24h": -1.2, "high_w": 3450, "low_w": 3350},
    {"stock_name": "TSLA", "value": 700.00, "change_24h": 3.5, "high_w": 720, "low_w": 680},
    {"stock_name": "FB", "value": 350.00, "change_24h": 0.9, "high_w": 360, "low_w": 340},
    {"stock_name": "NFLX", "value": 600.00, "change_24h": -2.3, "high_w": 620, "low_w": 580},
    {"stock_name": "NVDA", "value": 220.00, "change_24h": 1.8, "high_w": 230, "low_w": 210},
    {"stock_name": "INTC", "value": 55.00, "change_24h": -0.5, "high_w": 58, "low_w": 52},
    {"stock_name": "AMD", "value": 100.00, "change_24h": 2.7, "high_w": 105, "low_w": 95}
]

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def should_run():
    global last_run_time
    current_time = datetime.now()
    if current_time - last_run_time >= timedelta(minutes=3):
        last_run_time = datetime.now()
        return True
    else:
        return False

async def sync_initial_stocks(db: AsyncSession):
    for stock_data in stocks:
        result = await db.execute(select(Stock).filter(Stock.stock_name == stock_data["stock_name"]))
        db_stock = result.scalars().first()
        if db_stock:
            db_stock.high_w = stock_data["high_w"]
            db_stock.low_w = stock_data["low_w"]
        else:
            db_stock = Stock(stock_name=stock_data["stock_name"], high_w=stock_data["high_w"], low_w=stock_data["low_w"])
            db.add(db_stock)
        await db.commit()
        

async def decide_stock_values(db: Session):
    stocks = db.execute(Stock).all()
    for stock in stocks:
        low_threshold = stock.low_w + stock.low_w * 0.10
        high_threshold = stock.high_w + stock.high_w * 0.10
        nextval = random.uniform(low_threshold, high_threshold)
        # Assuming there is a corresponding StockValue entry that you want to update
        stock_value = db.execute(StockValue).filter(StockValue.stock_id == stock.id).first()
        if stock_value:
            stock_value.change_24h = (1 - (nextval / stock_value.value)) * 100
            stock_value.value = round(nextval, 2)
            db.commit()
        if stock_value.value < stock.low_w:
            stock.low_w = stock_value.value
        elif stock_value.value > stock.high_w:
            stock.high_w = stock_value.value
    db.commit()

async def sleep_in_db():
    print(engine.pool.status())  # 0 connections
    async with engine.connect() as connection:
        print(engine.pool.status())  # 1 connection
        while True:
            await connection.execute(text("select now();"))
            await asyncio.sleep(1)

async def startup_event():
    await create_tables()
    async with engine.begin() as conn:
        db = AsyncSession(bind=conn)
        await sync_initial_stocks(db)
    print("Started SQLAlchemy")

app.add_event_handler("startup", startup_event)

@app.get("/backend/updatestockdata")
async def root(db: Session = Depends(get_db)):
    if should_run():
        decide_stock_values(db)
    results = await db.execute(Stock).all()
    return results