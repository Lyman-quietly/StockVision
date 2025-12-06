from fastapi import APIRouter, HTTPException
from services.market_data import get_stock_history, get_stock_info
from services.news_data import get_stock_news
from analysis.sentiment import analyze_sentiment
import json

router = APIRouter(
    prefix="/stock",
    tags=["stock"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{ticker}/history")
async def read_stock_history(ticker: str, period: str = "1y", interval: str = "1d"):
    df = get_stock_history(ticker, period, interval)
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock data not found")
    # Convert DataFrame to JSON-compatible format (list of records)
    # Reset index to include Date
    df.reset_index(inplace=True)
    return df.to_dict(orient="records")

@router.get("/{ticker}/info")
async def read_stock_info(ticker: str):
    info = get_stock_info(ticker)
    if not info:
        raise HTTPException(status_code=404, detail="Stock info not found")
    return info

@router.get("/{ticker}/news")
async def read_stock_news(ticker: str):
    news = get_stock_news(ticker)
    # Enrich with sentiment
    for item in news:
        if 'title' in item:
            item['sentiment'] = analyze_sentiment(item['title'])
    return news
