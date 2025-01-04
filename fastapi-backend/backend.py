from fastapi import FastAPI

import json
import random

# Sample stock data
stocks = [
    {"symbol": "AAPL", "value": 150.00, "change_24h": 1.5, "high_52w": 182.94, "low_52w": 116.21},
    {"symbol": "MSFT", "value": 250.00, "change_24h": -0.8, "high_52w": 305.84, "low_52w": 213.43},
    {"symbol": "GOOGL", "value": 2800.00, "change_24h": 2.1, "high_52w": 2925.07, "low_52w": 2523.50},
    {"symbol": "AMZN", "value": 3400.00, "change_24h": -1.2, "high_52w": 3773.08, "low_52w": 2881.00},
    {"symbol": "TSLA", "value": 700.00, "change_24h": 3.5, "high_52w": 900.40, "low_52w": 546.98},
    {"symbol": "FB", "value": 350.00, "change_24h": 0.9, "high_52w": 384.33, "low_52w": 244.61},
    {"symbol": "NFLX", "value": 600.00, "change_24h": -2.3, "high_52w": 700.99, "low_52w": 478.54},
    {"symbol": "NVDA", "value": 220.00, "change_24h": 1.8, "high_52w": 346.47, "low_52w": 180.68},
    {"symbol": "INTC", "value": 55.00, "change_24h": -0.5, "high_52w": 68.49, "low_52w": 43.63},
    {"symbol": "AMD", "value": 100.00, "change_24h": 2.7, "high_52w": 164.46, "low_52w": 72.50}
]
 
app = FastAPI()

def updateStockValues():
    for stock in stocks:
        low_threshold = stock["low_52w"]+ stock["low_52w"] * 0.10
        high_threshold = stock["high_52w"] + stock["high_52w"] * 0.10

        nextval = random.uniform(low_threshold, high_threshold)

        stock["change_24h"] =  ( stock["value"] / nextval) - 1
        stock["value"] = round(nextval,2)
        
        if stock["value"] < stock["low_52w"]:
            stock["low_52w"] = stock["value"]
        elif stock["value"] > stock["high_52w"]:
            stock["high_52w"] = stock["value"]


@app.get("/backend/updatestockdata")
async def root():
    updateStockValues()
    return stocks