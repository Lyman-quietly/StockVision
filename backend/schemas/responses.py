from pydantic import BaseModel
from typing import List, Optional, Dict, Union

class StockHistoryItem(BaseModel):
    Date: str
    Open: float
    High: float
    Low: float
    Close: float
    Volume: int
    Dividends: Optional[float] = 0.0
    Stock_Splits: Optional[float] = 0.0

class NewsItem(BaseModel):
    uuid: str
    title: str
    publisher: str
    link: str
    providerPublishTime: Optional[int] = None
    type: Optional[str] = None
    sentiment: float = 0.0

class PredictionStats(BaseModel):
    model: str
    current_sma: Optional[List[float]] = None
    prediction_next_day: Optional[float] = None
    predictions: Optional[List[float]] = None
    forecast: Optional[List[float]] = None
    prediction: Optional[float] = None
    error: Optional[str] = None

class PredictionResponse(BaseModel):
    ticker: str
    statistical: Dict[str, PredictionStats]
    ml: Dict[str, PredictionStats]
