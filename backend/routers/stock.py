from fastapi import APIRouter, HTTPException
import uuid
from services.news_data import get_stock_news
from analysis.sentiment import analyze_sentiment
from schemas.responses import NewsItem
from typing import List

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

@router.get("/{ticker}/news", response_model=List[NewsItem])
async def read_stock_news(ticker: str):
    news = get_stock_news(ticker)
    # Enrich with sentiment
    enriched_news = []
    for item in news:
        # Map yfinance news dict to our schema
        sentiment_score = 0.0
        if 'title' in item:
            sentiment_score = analyze_sentiment(item['title'])
        
        news_uuid = item.get("uuid")
        if not news_uuid:
            news_uuid = str(uuid.uuid4())
        
        enriched_news.append(NewsItem(
            uuid=news_uuid,
            title=item.get("title", ""),
            publisher=item.get("publisher", ""),
            link=item.get("link", ""),
            providerPublishTime=item.get("providerPublishTime"),
            type=item.get("type"),
            sentiment=sentiment_score
        ))
    return enriched_news
