"""Convert aligned daily adjusted prices to completed Friday-ending weekly returns."""
import numpy as np
import pandas as pd


def weekly_returns(prices):
    """Use last available price per week; exclude unfinished final week.

    Supply adjusted prices and a timezone-naive local-market date index.
    Missing weeks are not filled. Returns require prices in consecutive weeks.
    The first weekly close is a baseline, not a return observation.
    """
    if not isinstance(prices.index, pd.DatetimeIndex) or prices.index.tz is not None:
        raise ValueError('Use timezone-naive market dates.')
    if prices.empty or prices.index.has_duplicates or prices.columns.has_duplicates:
        raise ValueError('Supply prices with unique dates and tickers.')
    prices = prices.sort_index().astype(float)
    if not np.isfinite(prices.to_numpy()).all() or (prices <= 0).any().any():
        raise ValueError('Prices must be aligned, finite and positive; clean missing data first.')
    closes = prices.resample('W-FRI').last()
    closes = closes.loc[closes.index <= prices.index.max().normalize()]
    result = closes.pct_change(fill_method=None).dropna(how='any')
    if len(result) < 2:
        raise ValueError('At least two complete weekly return observations are required.')
    return result
