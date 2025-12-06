import yfinance as yf

def get_stock_news(ticker: str) -> list:
    """
    Fetch news for a given ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        return news
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []
