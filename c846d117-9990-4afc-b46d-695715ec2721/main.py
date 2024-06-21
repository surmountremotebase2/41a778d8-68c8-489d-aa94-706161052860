from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
import pandas as pd
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets you're interested in
        self.tickers = ["SPY"]  # Example ticker

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        "1day"  # Daily interval for calculating VIX Fix

    def vix_fix(self, data):
        """
        Calculate VIX Fix for a given asset
        WVF = [(Highest Close in past 22 days - Low Today) / (Highest Close in past 22 days)] * 100
        """
        close_prices = [d["close"] for d in data]  # Extract close prices
        low_prices = [d["low"] for d in data]  # Extract low prices
        highest_close = pd.Series(close_prices).rolling(window=22).max()  # Find max of close prices over the past 22 days
        
        wvf = ((highest_close - pd.Series(low_prices)) / highest_close) * 100  # Calculate the Williams' VIX Fix
        return wvf.tolist()

    def run(self, data):
        """
        Buy signal based on VIX Fix
        Assuming a simple strategy where a higher VIX Fix value signals potential market bottom,
        hence a buying opportunity.
        """
        allocation = {}
        for ticker in self.tickers:
            wvf = self.vix_fix(data["ohlcv"][ticker])
            if len(wvf) > 0 and wvf[-1] > 30:  # Example threshold, customize based on backtesting
                allocation[ticker] = 1.0  # Fully allocate to this security
            else:
                allocation[ticker] = 0  # No allocation

        return TargetAllocation(allocation)