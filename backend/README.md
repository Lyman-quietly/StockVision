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
