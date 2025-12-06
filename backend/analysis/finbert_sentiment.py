from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch
from typing import Dict

class FinBertAnalyzer:
    """
    Singleton class for FinBERT Sentiment Analysis.
    Loads 'ProsusAI/finbert' model for financial sentiment classification.
    """
    _instance = None
    _pipeline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FinBertAnalyzer, cls).__new__(cls)
            try:
                # Load pipeline - this handles tokenization and model inference automatically
                # Run on CPU by default. Set device=0 for GPU if torch.cuda.is_available()
                cls._pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert", return_all_scores=True)
            except Exception as e:
                print(f"Error loading FinBERT: {e}")
                cls._pipeline = None
        return cls._instance

    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze financial text sentiment.
        Returns dictionary with probabilities for 'positive', 'negative', 'neutral'
        and a 'composite' score (-1 to 1).
        """
        if not text or not self._pipeline:
            return {"positive": 0.0, "negative": 0.0, "neutral": 0.0, "composite": 0.0}

        try:
            # Result format: [[{'label': 'positive', 'score': 0.9}, ...]]
            results = self._pipeline(text)[0]
            
            scores = {item['label']: item['score'] for item in results}
            
            pos = scores.get('positive', 0.0)
            neg = scores.get('negative', 0.0)
            neu = scores.get('neutral', 0.0)
            
            # Composite Score: Simple heuristic
            # Positive contributes +1, Negative -1. Weighted by their probability.
            composite = pos - neg
            
            return {
                "positive": pos,
                "negative": neg,
                "neutral": neu,
                "composite": composite
            }
        except Exception as e:
            print(f"FinBERT Analysis Error: {e}")
            return {"positive": 0.0, "negative": 0.0, "neutral": 0.0, "composite": 0.0}

# Global instance for easy import
sentiment_analyzer = FinBertAnalyzer()
