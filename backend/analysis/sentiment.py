from textblob import TextBlob

def analyze_sentiment(text: str) -> float:
    """
    Analyze the sentiment of a text string.
    Returns a polarity score between -1.0 (negative) and 1.0 (positive).
    """
    if not text:
        return 0.0
    blob = TextBlob(text)
    return blob.sentiment.polarity
