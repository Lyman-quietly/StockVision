import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from typing import Dict, Tuple, Any
from .technical import TechnicalAnalysis

def prepare_data(data: pd.DataFrame, lag: int = 5) -> Tuple[pd.DataFrame, pd.Series, pd.Series, pd.DataFrame]:
    """
    Prepare data for ML models.
    Target: Next Day's Close (t+1)
    Features (at t): Technical Indicators(t) + Close(t) + Lags(t-1, ...)
    """
    df = data.copy()
    
    # 1. Add Technical Indicators (calculated on current data)
    # RSI_14 @ t uses Close @ t
    df = TechnicalAnalysis.add_all_indicators(df)
    
    # 2. Create Lag Features
    # lag_1 = Close @ t-1
    for i in range(1, lag + 1):
        df[f'lag_{i}'] = df['Close'].shift(i)
        
    # 3. Define Target (Next Day Close)
    # Target @ t = Close @ t+1
    df['Target'] = df['Close'].shift(-1)
    
    # 4. Define Feature Columns
    # We use all numeric columns except Target and original OHLCV (optional)
    # For simplicity, we keep 'Close' as a feature (current price) and all indicators/lags.
    # Exclude non-numeric and Target.
    exclude_cols = ['Target', 'Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits']
    feature_cols = [c for c in df.columns if c not in exclude_cols]
    
    # 5. Handle NaNs
    # Indicators introduce NaNs at the start.
    # Target shift introduces NaN at the end (Last row).
    # We need the Last Row for "Next Day Prediction", but we can't train on it.
    
    # Drop rows where Features are NaN (start of data)
    # We must NOT drop the last row yet (where Target is NaN) if we want to use it for prediction.
    # So we use subset=feature_cols to drop initial NaNs.
    df_clean = df.dropna(subset=feature_cols).copy()
    
    if df_clean.empty:
         raise ValueError("Not enough data after calculating indicators")

    # Split:
    # Training Data: All rows where Target is NOT NaN
    train_df = df_clean.dropna(subset=['Target'])
    X_train = train_df[feature_cols]
    y_train = train_df['Target']
    
    # Prediction Input: The very last row (where Target IS NaN, or just the last available row of features)
    # This row represents "Today", used to predict "Tomorrow".
    last_row = df_clean.iloc[[-1]][feature_cols]
    
    return X_train, y_train, last_row, df_clean

def train_and_predict_rf(data: pd.DataFrame) -> Dict[str, Any]:
    """Random Forest Prediction"""
    try:
        X, y, last_row, _ = prepare_data(data)
        
        # Train
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Predict Next Day
        prediction = model.predict(last_row)
        
        return {
            "model": "Random Forest",
            "prediction": float(prediction[0])
        }
    except Exception as e:
        return {"error": str(e)}

def train_and_predict_xgb(data: pd.DataFrame) -> Dict[str, Any]:
    """XGBoost Prediction"""
    try:
        X, y, last_row, _ = prepare_data(data)
        
        model = XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model.fit(X, y)
        
        prediction = model.predict(last_row)
        
        return {
            "model": "XGBoost",
            "prediction": float(prediction[0])
        }
    except Exception as e:
        print(f"XGB Error: {e}")
        return {"error": str(e)}

def train_and_predict_svr(data: pd.DataFrame) -> Dict[str, Any]:
    """Support Vector Regression Prediction"""
    try:
        X, y, last_row, _ = prepare_data(data)
        
        model = SVR(C=1000, gamma=0.1)
        model.fit(X, y)
        
        prediction = model.predict(last_row)
        
        return {
            "model": "SVR",
            "prediction": float(prediction[0])
        }
    except Exception as e:
        return {"error": str(e)}
