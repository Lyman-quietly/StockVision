import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from typing import Dict, List

def prepare_data(data: pd.DataFrame, lag: int = 5):
    """
    Prepare data for ML models by creating lag features.
    Predict Next Day Close based on previous 'lag' days.
    """
    df = data[['Close']].copy()
    for i in range(1, lag + 1):
        df[f'lag_{i}'] = df['Close'].shift(i)
    
    df.dropna(inplace=True)
    
    X = df[[f'lag_{i}' for i in range(1, lag + 1)]]
    y = df['Close']
    return X, y, df

def train_and_predict_rf(data: pd.DataFrame) -> Dict:
    """Random Forest Prediction"""
    try:
        X, y, df = prepare_data(data)
        if len(X) < 10: return {"error": "Not enough data"}

        # Train on all available data for the 'latest' prediction
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Predict next day using the very last available window
        last_window = np.array([data['Close'].iloc[-5:].values[::-1]]) # flip to match lag_1, lag_2...
        # Note: simplistic feature mapping, ensuring shape matches
        if last_window.shape[1] != 5:
             # handle edge case
             return {"error": "Data shape mismatch"}

        prediction = model.predict(last_window)
        
        return {
            "model": "Random Forest",
            "prediction": float(prediction[0])
        }
    except Exception as e:
        return {"error": str(e)}

def train_and_predict_xgb(data: pd.DataFrame) -> Dict:
    """XGBoost Prediction"""
    try:
        X, y, df = prepare_data(data)
        if len(X) < 10: return {"error": "Not enough data"}
        
        model = XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model.fit(X, y)
        
        last_window = pd.DataFrame([data['Close'].iloc[-5:].values[::-1]], columns=X.columns)
        
        prediction = model.predict(last_window)
        
        return {
            "model": "XGBoost",
            "prediction": float(prediction[0])
        }
    except Exception as e:
        print(f"XGB Error: {e}")
        return {"error": str(e)}

def train_and_predict_svr(data: pd.DataFrame) -> Dict:
    """Support Vector Regression Prediction"""
    try:
        X, y, df = prepare_data(data)
        if len(X) < 10: return {"error": "Not enough data"}
        
        model = SVR(C=1000, gamma=0.1)
        model.fit(X, y)
        
        last_window = np.array([data['Close'].iloc[-5:].values[::-1]])
        
        prediction = model.predict(last_window)
        
        return {
            "model": "SVR",
            "prediction": float(prediction[0])
        }
    except Exception as e:
        return {"error": str(e)}
