"""Validate Yahoo daily histories without filling prices or mixing data sources."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import threading
import time
import numpy as np
import pandas as pd


def request_window(country, years, as_of=None):
    """Exclude today's session until 18:00 in the selected market timezone."""
    if country not in ('United States', 'Japan') or years not in (5, 8):
        raise ValueError('Yahoo mode supports United States/Japan and 5/8 years.')
    zone = ZoneInfo('America/New_York' if country == 'United States' else 'Asia/Tokyo')
    now = as_of if as_of is not None else datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('Supply a timezone-aware retrieval time.')
    local = now.astimezone(zone)
    end = local.date() + timedelta(days=1 if local.hour >= 18 else 0)
    start = (pd.Timestamp(end) - pd.DateOffset(years=years)).date()
    return str(start), str(end)


def yahoo_symbol(ticker, country):
    ticker = str(ticker).strip()
    if country == 'Japan':
        return ticker + '.T'
    if country == 'United States':
        return ticker.replace('.', '-')
    raise ValueError('Philippine stocks use the stored dataset.')


_request_lock = threading.Lock()
_cooldown_until = 0.0
_last_request = 0.0


class ProviderCooldown(RuntimeError):
    """A temporary provider limit; not evidence that the stock is unsupported."""


def download_one(symbol, start, end):
    # Import only when used; the stored-data workflow has no Yahoo dependency.
    import yfinance as yf
    global _cooldown_until, _last_request
    with _request_lock:
        if time.monotonic() < _cooldown_until:
            raise ProviderCooldown('Yahoo requests are paused after a rate limit.')
        # Serialize requests and leave a short gap. This does not guarantee access.
        pause = 0.4 - (time.monotonic() - _last_request)
        if pause > 0:
            time.sleep(pause)
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(start=start, end=end, interval='1d', auto_adjust=False,
                                     actions=False, repair=False, raise_errors=True, timeout=12)
            metadata = ticker.get_history_metadata()
            return history, metadata.get('currency')
        except Exception as exc:
            if type(exc).__name__ == 'YFRateLimitError':
                _cooldown_until = time.monotonic() + 15 * 60
            raise
        finally:
            _last_request = time.monotonic()



def collect_yahoo(info, country, years, start, end, fetcher=download_one):
    """Fetch a candidate subset; return aligned prices, metadata, coverage audit.

    Require source-adjusted closes, correct currency, long and recent coverage.
    A failed ticker is excluded. Three consecutive request failures stop a batch
    to avoid repeatedly calling a blocked/unavailable service. Exclusions are
    reported explicitly. No fixed-snapshot prices are mixed into Yahoo prices.
    """
    expected = 'USD' if country == 'United States' else 'JPY'
    rows, valid = [], {}
    failed_run = 0
    for ticker in info.index.astype(str):
        symbol = yahoo_symbol(ticker, country)
        row = dict(ticker=ticker, yahoo_symbol=symbol, status='Excluded', reason='',
                   first_date='', last_date='', daily_observations=0, currency='')
        if failed_run >= 3:
            row['reason'] = 'Not requested: batch stopped after provider limits or repeated download failures.'
            rows.append(row)
            continue
        try:
            history, currency = fetcher(symbol, start, end)
            if history is None or history.empty:
                raise RuntimeError('No daily history returned.')
            failed_run = 0
        except Exception as exc:
            failed_run += 1
            if type(exc).__name__ in ('YFRateLimitError', 'ProviderCooldown'):
                failed_run = 3
            # Do not expose URLs, tokens, or provider error bodies to visitors.
            row['reason'] = f'Download failed ({type(exc).__name__}).'
            rows.append(row)
            continue
        try:
            row['currency'] = currency or ''
            if currency != expected:
                raise ValueError(f'Currency must be {expected}; returned {currency or "unknown"}.')
            if 'Adj Close' not in history:
                raise ValueError('Adjusted close is unavailable; raw close is not substituted.')
            prices = pd.to_numeric(history['Adj Close'], errors='coerce').copy()
            index = pd.DatetimeIndex(prices.index)
            if index.tz is not None:
                index = index.tz_localize(None)
            prices.index = index.normalize()
            prices = prices.loc[(prices.index >= pd.Timestamp(start)) &
                                (prices.index < pd.Timestamp(end))].sort_index()
            if prices.empty:
                raise ValueError('No observations inside the requested date window.')
            row.update(first_date=str(prices.index.min().date()),
                       last_date=str(prices.index.max().date()), daily_observations=len(prices))
            if prices.index.has_duplicates:
                raise ValueError('Duplicate trading dates.')
            if not np.isfinite(prices).all() or prices.le(0).any():
                raise ValueError('Missing, nonfinite or nonpositive adjusted prices.')
            if prices.index.dayofweek.isin([5, 6]).any():
                raise ValueError('Unexpected weekend observations.')
            if prices.index.min() > pd.Timestamp(start) + pd.Timedelta(days=14):
                raise ValueError(f'History does not cover the requested {years}-year window.')
            if prices.index.max() < pd.Timestamp(end) - pd.Timedelta(days=10):
                raise ValueError('Latest price is more than 10 calendar days behind the cutoff.')
            if len(prices) < years * 220:
                raise ValueError(f'Too few daily observations for {years} years.')
            valid[ticker] = prices
            row.update(status='Eligible', reason='')
        except (ValueError, TypeError, KeyError) as exc:
            row['reason'] = str(exc)
        rows.append(row)
    audit = pd.DataFrame(rows)
    if not valid:
        return pd.DataFrame(), info.iloc[:0].copy(), audit
    panel = pd.concat(valid, axis=1).sort_index().rename_axis('date')
    # Use the union of observed market dates to detect gaps; never forward-fill.
    incomplete = panel.columns[panel.isna().any()].tolist()
    if incomplete:
        for ticker in incomplete:
            audit.loc[audit.ticker.eq(ticker), ['status', 'reason']] = [
                'Excluded', 'Missing prices on dates observed for other candidates.']
        panel = panel.drop(columns=incomplete)
    return panel, info.loc[panel.columns].copy(), audit
