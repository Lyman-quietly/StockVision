import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from typing import Dict, List

def predict_moving_average(data: pd.DataFrame, window: int = 30) -> Dict[str, List[float]]:
    """
    Predict using Simple Moving Average.
    Returns the last 'window' days of moving averages and a projection.
    """
    if 'Close' not in data.columns:
        return {}
    
    # Calculate SMA
    sma = data['Close'].rolling(window=window).mean()
    
    # Project next day (naive approach: last SMA value)
    last_sma = sma.iloc[-1]
    
    return {
        "model": "Simple Moving Average",
        "current_sma": sma.tail(5).tolist(),
        "prediction_next_day": float(last_sma) if not np.isnan(last_sma) else 0.0
    }

def predict_linear_trend(data: pd.DataFrame, days_forward: int = 5) -> Dict[str, float]:
    """
    Predict future price using Linear Regression on the last 60 days.
    """
    if 'Close' not in data.columns or len(data) < 2:
        return {}
    
    # Use last 60 days
    recent_data = data.tail(60).copy()
    recent_data['Day'] = range(len(recent_data))
    
    X = recent_data[['Day']]
    y = recent_data['Close']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next days
    next_days = np.array([[len(recent_data) + i] for i in range(days_forward)])
    predictions = model.predict(next_days)
    
    return {
        "model": "Linear Trend",
        "predictions": predictions.tolist()
    }

def predict_arima(data: pd.DataFrame, order=(1,1,1)) -> Dict[str, List[float]]:
    """
    Predict using ARIMA model.
    """
    if 'Close' not in data.columns:
        print("No Close column")
        return {}
    
    try:
        # Fit model on closing price
        # Using a smaller subset for speed if needed, e.g. last 1 year
        series = data['Close']
        model = ARIMA(series, order=order)
        model_fit = model.fit()
        
        # Forecast next 5 days
        forecast = model_fit.forecast(steps=5)
        
        return {
            "model": "ARIMA",
            "forecast": forecast.tolist()
        }
    except Exception as e:
        print(f"ARIMA Error: {e}")
        return {"error": str(e)}
