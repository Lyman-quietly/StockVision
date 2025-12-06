from analysis.sentiment import analyze_sentiment

def test_analyze_sentiment_positive():
    text = "Stock market rallies on good news"
    # Expect positive polarity
    score = analyze_sentiment(text)
    assert score > 0

def test_analyze_sentiment_negative():
    text = "Stock market crashes on bad news"
    # Expect negative polarity
    score = analyze_sentiment(text)
    assert score < 0

def test_analyze_sentiment_neutral():
    text = "Stock market flows"
    # Expect approximately neutral
    score = analyze_sentiment(text)
    assert -0.5 < score < 0.5
