from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime, timedelta
from model import Stock, StockValue
import schemas
import stock
from db import engine, create_tables, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging
import asyncio

last_run_time = datetime.now()
app = FastAPI()
app.include_router(stock.router)

stocks = [
    {"stock_name": "AAPL", "value": 150.00, "percentage_change": 1.5, "high_w": 155, "low_w": 145},
    {"stock_name": "MSFT", "value": 250.00, "percentage_change": -0.8, "high_w": 260, "low_w": 240},
    {"stock_name": "GOOGL", "value": 2800.00, "percentage_change": 2.1, "high_w": 2850, "low_w": 2750},
    {"stock_name": "AMZN", "value": 3400.00, "percentage_change": -1.2, "high_w": 3450, "low_w": 3350},
    {"stock_name": "TSLA", "value": 700.00, "percentage_change": 3.5, "high_w": 720, "low_w": 680},
    {"stock_name": "FB", "value": 350.00, "percentage_change": 0.9, "high_w": 360, "low_w": 340},
    {"stock_name": "NFLX", "value": 600.00, "percentage_change": -2.3, "high_w": 620, "low_w": 580},
    {"stock_name": "NVDA", "value": 220.00, "percentage_change": 1.8, "high_w": 230, "low_w": 210},
    {"stock_name": "INTC", "value": 55.00, "percentage_change": -0.5, "high_w": 58, "low_w": 52},
    {"stock_name": "AMD", "value": 100.00, "percentage_change": 2.7, "high_w": 105, "low_w": 95}
]

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def sync_initial_stocks(db: AsyncSession):
    for stock_data in stocks:
        result = await db.execute(select(Stock).filter(Stock.stock_name == stock_data["stock_name"]))
        db_stock = result.scalars().first()
        if db_stock:
            db_stock.high_w = stock_data["high_w"]
            db_stock.low_w = stock_data["low_w"]
            db_stock.percentage_change = stock_data["percentage_change"]  # Update percentage_change
        else:
            db_stock = Stock(
                stock_name=stock_data["stock_name"], 
                high_w=stock_data["high_w"], 
                low_w=stock_data["low_w"],
                percentage_change=stock_data["percentage_change"],
                latest_value=stock_data["value"] # Set initial percentage_change
            )
            db.add(db_stock)
            await db.commit()
            await db.refresh(db_stock)
        new_value = StockValue(stock_id=db_stock.id, value=stock_data["value"], timestamp=datetime.now())
        db.add(new_value)
        await db.commit()

async def decide_stock_values(db: AsyncSession):
    result_all_stocks_in_db = await db.execute(select(Stock))
    all_stocks_in_db = result_all_stocks_in_db.scalars().all()
    stock_index = 1
    
    for stock in all_stocks_in_db:
        result_stockvalues = await db.execute(select(StockValue))
        stockvalues = result_stockvalues.scalars().all()
        stockvalues = [stockvalue for stockvalue in stockvalues if stockvalue.stock_id == stock_index]
        if stockvalues:
            db_stockvalue = stockvalues[-1]  # Get the most recent stock value entry for the stock
            low_threshold = db_stockvalue.value - db_stockvalue.value * 0.10
            high_threshold = db_stockvalue.value + db_stockvalue.value * 0.10
            nextval = random.uniform(low_threshold, high_threshold)
            nextval = int(round(nextval))
            new_value = StockValue(stock_id=db_stockvalue.stock_id, value=nextval, timestamp=datetime.now())
            percentage_change = ((nextval - db_stockvalue.value) / db_stockvalue.value) * 100
            db.add(new_value)
            await db.commit()
            result = await db.execute(select(Stock).filter(Stock.id == stock_index))
            stock = result.scalars().first()
            print(stock.stock_name)
            if nextval < stock.low_w:
                stock.low_w = nextval
            if nextval > stock.high_w:
                stock.high_w = nextval
            stock.latest_value = nextval
            stock.percentage_change = round(percentage_change,1)
            db.add(stock)
            await db.commit()
            await db.refresh(stock)
        else:
            # If no stock values are found, create a new stock value entry and set initial values
            initial_value = stock.low_w
            new_value = StockValue(stock_id=stock.id, value=initial_value, timestamp=datetime.now())
            db.add(new_value)
            await db.commit()    
            stock.latest_value = initial_value
            stock.percentage_change = 0.0 
            db.add(stock)
            await db.commit()
        stock_index += 1
    
    print("Stock values updated successfully")

async def background_task():
    while True:
        async with engine.begin() as conn:
            async with AsyncSession(bind=conn) as db:
                await decide_stock_values(db)
        await asyncio.sleep(30)  # Sleep for 30 seconds

async def startup_event():
    await create_tables()
    async with engine.begin() as conn:
        async with AsyncSession(bind=conn) as db:
            await sync_initial_stocks(db)
    asyncio.create_task(background_task())  # Start the background task

app.add_event_handler("startup", startup_event)
