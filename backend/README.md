# StockVision Backend

## Overview
This is the backend service for the StockVision desktop application. It provides market data analysis, news sentiment scores, and multiple stock price prediction models.

## Architecture
- **Framework**: FastAPI
- **Data Source**: yfinance
- **ML/Stats**: Scikit-Learn, Statsmodels, XGBoost, TextBlob

## Setup

1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Server**:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation
Once running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

## Directory Structure
- `analysis/`: Core logic for statistics and ML models.
- `core/`: Configuration and settings.
- `routers/`: API route definitions.
- `schemas/`: Pydantic models for request/response validation.
- `services/`: External data fetching.
- `tests/`: Unit tests.

## Roadmap: Path to Profitability
We are evolving StockVision into a trading assistant capable of generating profit.
1. **Advanced Technical Analysis**: Integration of momentum, trend, and volatility indicators (RSI, MACD, Bollinger Bands).
2. **Enhanced ML Models**: Feature engineering with technical indicators and hyperparameter tuning.
3. **Sentiment Analysis 2.0**: Financial-specific sentiment analysis using Transformer models.
4. **Backtesting Engine**: A framework to validate strategies against historical data.
5. **Signal Generation**: Clear BUY/SELL/HOLD signals instead of just raw price predictions.
