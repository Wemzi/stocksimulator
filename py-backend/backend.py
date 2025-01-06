from fastapi import FastAPI
import json
import random
from datetime import datetime, timedelta
from model import Stock
import schemas
import model
import stock
from db import DATABASE_URL, engine, Base, SessionLocal
from sqlalchemy import inspect
import sys
import logging

# Store the last run time
last_run_time = datetime.now()

def should_run():
    global last_run_time
    # Get the current time
    current_time = datetime.now()
    # Check if 5 minutes have passed since the last run
    if current_time - last_run_time >= timedelta(minutes=3):
        last_run_time = datetime.now()
        return True
    else:
        return False

stocks = [
    {"symbol": "AAPL", "value": 150.00, "change_24h": 1.5, "high_w": 155.00, "low_w": 145.00},
    {"symbol": "MSFT", "value": 250.00, "change_24h": -0.8, "high_w": 260.00, "low_w": 240.00},
    {"symbol": "GOOGL", "value": 2800.00, "change_24h": 2.1, "high_w": 2850.00, "low_w": 2750.00},
    {"symbol": "AMZN", "value": 3400.00, "change_24h": -1.2, "high_w": 3450.00, "low_w": 3350.00},
    {"symbol": "TSLA", "value": 700.00, "change_24h": 3.5, "high_w": 720.00, "low_w": 680.00},
    {"symbol": "FB", "value": 350.00, "change_24h": 0.9, "high_w": 360.00, "low_w": 340.00},
    {"symbol": "NFLX", "value": 600.00, "change_24h": -2.3, "high_w": 620.00, "low_w": 580.00},
    {"symbol": "NVDA", "value": 220.00, "change_24h": 1.8, "high_w": 230.00, "low_w": 210.00},
    {"symbol": "INTC", "value": 55.00, "change_24h": -0.5, "high_w": 58.00, "low_w": 52.00},
    {"symbol": "AMD", "value": 100.00, "change_24h": 2.7, "high_w": 105.00, "low_w": 95.00}
]
 
app = FastAPI()
app.include_router(stock.router)

def decideStockValues():
    for stock in stocks:
        low_threshold = stock["low_w"]+ stock["low_w"] * 0.10
        high_threshold = stock["high_w"] + stock["high_w"] * 0.10
        nextval = random.uniform(low_threshold, high_threshold)
        stock["change_24h"] =  (1 - (nextval / stock["value"])) * 100 
        stock["value"] = round(nextval,2)
        
        if stock["value"] < stock["low_w"]:
            stock["low_w"] = stock["value"]
        elif stock["value"] > stock["high_w"]:
            stock["high_w"] = stock["value"]

async def sleep_in_db():
        print(engine.pool.status()) # 0 connections
        async with engine.connect() as connection:
            print(engine.pool.status()) # 1 connections
            while True:
                await connection.execute(text("select now();"))
                await asyncio.sleep(1)

@app.on_event("startup") 
async def startup(): 
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/backend/updatestockdata")
async def root():
    if should_run():
        decideStockValues()
    return stocks