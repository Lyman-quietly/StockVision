import pandas as pd
import pandas_ta as ta
from typing import List

class TechnicalAnalysis:
    """
    Technical Analysis engine using pandas-ta.
    Wraps common indicators for easy application to DataFrames.
    """

    @staticmethod
    def add_rsi(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """Adds Relative Strength Index (RSI)."""
        if 'Close' not in df.columns:
            return df
        # pandas-ta appends columns automatically with specific names, e.g. RSI_14
        df.ta.rsi(length=length, append=True)
        return df

    @staticmethod
    def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Adds Moving Average Convergence Divergence (MACD)."""
        if 'Close' not in df.columns:
            return df
        # Columns: MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        df.ta.macd(fast=fast, slow=slow, signal=signal, append=True)
        return df

    @staticmethod
    def add_bollinger_bands(df: pd.DataFrame, length: int = 20, std: float = 2.0) -> pd.DataFrame:
        """Adds Bollinger Bands."""
        if 'Close' not in df.columns:
            return df
        # Columns: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0
        df.ta.bbands(length=length, std=std, append=True)
        return df

    @staticmethod
    def add_atr(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
        """Adds Average True Range (ATR)."""
        if not all(col in df.columns for col in ['High', 'Low', 'Close']):
            return df
        # Columns: ATRr_14
        df.ta.atr(length=length, append=True)
        return df

    @classmethod
    def add_all_indicators(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Adds all supported indicators to the DataFrame."""
        df = df.copy() # Avoid modifying original if passed by reference
        cls.add_rsi(df)
        cls.add_macd(df)
        cls.add_bollinger_bands(df)
        cls.add_atr(df)
        return df
