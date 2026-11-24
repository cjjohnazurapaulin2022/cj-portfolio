"""Describe the existing two-stage selection and its in-sample stock history.

This module reports results only. It does not select stocks or change weights.
"""
import numpy as np
import pandas as pd


def stock_insights(weekly, tickers, industries, selected_industries, result,
                   objective, preference=.5, stock_risk_limit=None):
    """Use exactly the candidate screen/scoring rules of core.optimizer."""
    tickers, industries = list(tickers), list(industries)
    r = weekly.loc[:, tickers].to_numpy(dtype=float)
    if r.shape[0] < 2 or not np.isfinite(r).all() or (r < -1).any():
        raise ValueError('Insights require finite aligned weekly simple returns.')
    sd = r.std(axis=0, ddof=1)
    eligible = [i for i, industry in enumerate(industries)
                if industry in selected_industries and
                (stock_risk_limit is None or sd[i] <= stock_risk_limit)]
    eligible.sort(key=lambda i: tickers[i])
    a = r[:, eligible]
    mu = a.mean(axis=0)
    mad = np.abs(a - mu).mean(axis=0)
    def scaled(v):
        return (v-v.min())/np.ptp(v) if np.ptp(v) > 1e-12 else np.zeros_like(v)
    if objective == 'return':
        score = mu
    elif objective == 'risk':
        score = -mad
    elif objective == 'balanced':
        score = preference*scaled(mu) - (1-preference)*scaled(mad)
    else:
        raise ValueError('Unknown selection objective.')
    candidates = pd.DataFrame({
        'ticker': [tickers[i] for i in eligible],
        'industry': [industries[i] for i in eligible],
        'mean': mu, 'mad': mad, 'sd': sd[eligible], 'score': score,
    }).set_index('ticker')
    candidates['industry_rank'] = candidates.groupby('industry')['score'].rank(
        ascending=False, method='min').astype(int)
    candidates['industry_count'] = candidates.groupby('industry')['score'].transform('size')
    chosen = [row['ticker'] for row in result['allocation']]
    if not set(chosen).issubset(candidates.index):
        raise ValueError('Selected stocks do not match the eligible candidate set.')
    explanations = candidates.loc[chosen].copy()
    selected_returns = weekly.loc[:, chosen]
    # Include the preceding Friday-ending baseline at 100, so the first return
    # is counted and the entire line agrees with the cumulative-return table.
    baseline = pd.Timestamp(weekly.index.min()) - pd.Timedelta(days=7)
    normalized = (1 + selected_returns).cumprod()*100
    normalized = pd.concat([
        pd.DataFrame(100., index=pd.DatetimeIndex([baseline]), columns=chosen),
        normalized,
    ]).rename_axis('Week ending')
    performance = pd.DataFrame({
        'Cumulative return (%)': (normalized.iloc[-1]/100 - 1)*100,
        'Average weekly return (%)': selected_returns.mean()*100,
        'Weekly volatility (%)': selected_returns.std(ddof=1)*100,
        'Weekly MAD (%)': selected_returns.sub(selected_returns.mean()).abs().mean()*100,
    }).loc[chosen]
    return explanations, performance, normalized
