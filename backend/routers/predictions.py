from fastapi import APIRouter, HTTPException
from services.market_data import get_stock_history
from analysis.statistical_models import predict_moving_average, predict_linear_trend, predict_arima
from analysis.ml_models import train_and_predict_rf, train_and_predict_xgb, train_and_predict_svr

router = APIRouter(
    prefix="/predict",
    tags=["predictions"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{ticker}")
async def get_predictions(ticker: str):
    # Fetch ample data for training/stats
    df = get_stock_history(ticker, period="2y", interval="1d")
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock data not found")
    
    # Run all models
    results = {
        "ticker": ticker,
        "statistical": {
            "moving_average": predict_moving_average(df),
            "linear_trend": predict_linear_trend(df),
            "arima": predict_arima(df)
        },
        "ml": {
            "random_forest": train_and_predict_rf(df),
            "xgboost": train_and_predict_xgb(df),
            "svr": train_and_predict_svr(df)
        }
    }
    
    return results
