"""Validate user-supplied daily adjusted prices; never fill missing prices."""
from io import BytesIO
import numpy as np
import pandas as pd

COLUMNS = ['date', 'ticker', 'company', 'industry', 'currency', 'adjusted_close']


def load_csv(data, currency, today=None):
    if len(data) > 20 * 1024 * 1024:
        raise ValueError('CSV must be at most 20 MB.')
    try:
        df = pd.read_csv(BytesIO(data), dtype=str, keep_default_na=False)
    except Exception as exc:
        raise ValueError('Cannot read this CSV. Save it as a UTF-8 comma-separated CSV.') from exc
    df.columns = df.columns.str.strip().str.lower()
    if df.columns.has_duplicates:
        raise ValueError('CSV column names must be unique.')
    if not set(COLUMNS).issubset(df.columns):
        raise ValueError('Required columns: ' + ', '.join(COLUMNS))
    df = df[COLUMNS].copy()
    if df.empty:
        raise ValueError('The CSV has no price rows.')
    for col in COLUMNS:
        df[col] = df[col].str.strip()
        if df[col].eq('').any():
            raise ValueError(f'Column {col} contains empty values.')
    df['currency'] = df['currency'].str.upper()
    if not df['currency'].eq(currency).all():
        raise ValueError(f'All rows must use {currency}, matching the selected country. No currency conversion is performed.')
    if df['ticker'].str.upper().eq('CASH').any():
        raise ValueError('CASH is reserved for the cash allocation row.')
    if not df['date'].str.fullmatch(r'\d{4}-\d{2}-\d{2}').all():
        raise ValueError('Dates must use YYYY-MM-DD, without times.')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
    if df['date'].isna().any():
        raise ValueError('The CSV contains invalid dates.')
    today = pd.Timestamp(today if today is not None else pd.Timestamp.now(tz='UTC').date()).normalize()
    if (df['date'] > today).any():
        raise ValueError('Future price dates are not allowed.')
    if df.duplicated(['date', 'ticker']).any():
        raise ValueError('Duplicate date/ticker rows found. Keep exactly one price per stock per date.')
    for col in ['company', 'industry', 'currency']:
        if df.groupby('ticker')[col].nunique().gt(1).any():
            raise ValueError(f'Each ticker must have one consistent {col}.')
    df['adjusted_close'] = pd.to_numeric(df['adjusted_close'], errors='coerce')
    if not np.isfinite(df['adjusted_close']).all() or df['adjusted_close'].le(0).any():
        raise ValueError('Adjusted prices must be positive numbers without currency symbols or thousands separators.')
    cutoff = today - pd.DateOffset(years=3)
    df = df[df['date'].ge(cutoff)].copy()
    if df.empty:
        raise ValueError('No prices fall within the latest three years.')
    if df['ticker'].nunique() > 600:
        raise ValueError('Upload at most 600 stocks per market.')
    return df


def aligned_prices(df, selected):
    subset = df[df['industry'].isin(selected)]
    if subset.empty:
        raise ValueError('No stocks belong to the selected industries.')
    prices = subset.pivot(index='date', columns='ticker', values='adjusted_close').sort_index()
    if prices.isna().any().any():
        raise ValueError('Selected stocks have missing or mismatched daily dates. Supply a common trading-date range with a valid price for every selected candidate. Missing prices are not filled or silently dropped.')
    meta = subset.drop_duplicates('ticker').set_index('ticker').loc[prices.columns]
    return prices, meta
