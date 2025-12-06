import uuid
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException


from schemas.responses import NewsItem
from services.market_data import get_stock_history, get_stock_info
from services.news_data import get_stock_news

router = APIRouter(
    prefix="/stock",
    tags=["stock"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{ticker}/history")
async def read_stock_history(
    ticker: str, period: str = "1y", interval: str = "1d"
) -> List[Dict[str, Any]]:
    """
    Fetch historical stock data.
    """
    df = get_stock_history(ticker, period, interval)
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock data not found")
    
    # Convert DataFrame to JSON-compatible format (list of records)
    # Reset index to include Date
    df.reset_index(inplace=True)
    # Pandas to_dict returns list of dicts, but type inference needs help sometimes
    return df.to_dict(orient="records") # type: ignore


@router.get("/{ticker}/info")
async def read_stock_info(ticker: str) -> Dict[str, Any]:
    """
    Fetch basic stock information.
    """
    info = get_stock_info(ticker)
    if not info:
        raise HTTPException(status_code=404, detail="Stock info not found")
    return info


@router.get("/{ticker}/news", response_model=List[NewsItem])
async def read_stock_news(ticker: str) -> List[NewsItem]:
    """
    Fetch and analyze news for a specific stock ticker.
    """
    news = get_stock_news(ticker)
    # Enrich with sentiment
    enriched_news = []
    
    # Import here to avoid circular dependencies if any, or at top level
    from analysis.finbert_sentiment import sentiment_analyzer

    for item in news:
        # Map yfinance news dict to our schema
        sentiment_result = {"composite": 0.0}
        if "title" in item:
            sentiment_result = sentiment_analyzer.analyze(item["title"])
        
        news_uuid = item.get("uuid")
        if not news_uuid:
            news_uuid = str(uuid.uuid4())
        
        enriched_news.append(NewsItem(
            uuid=news_uuid,
            title=item.get("title", ""),
            publisher=item.get("publisher", ""),
            link=item.get("link", ""),
            providerPublishTime=item.get("providerPublishTime"),
            type=item.get("type"), # Could use sentiment label here if desired
            sentiment=sentiment_result["composite"]
        ))
    return enriched_news

