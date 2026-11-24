import unittest
from datetime import datetime, timezone
import pandas as pd
import numpy as np
from core.market_data import collect_yahoo, yahoo_symbol, request_window

class MarketDataTests(unittest.TestCase):
    def setUp(self):
        self.start, self.end = '2021-11-24', '2026-11-24'
        self.dates = pd.bdate_range(self.start, '2026-11-23')
        self.info = pd.DataFrame({'ticker':['AAPL','MSFT'], 'company':['Apple','Microsoft'],
                                  'industry':['Hardware','Software']}).set_index('ticker')
        self.hist = pd.DataFrame({'Adj Close': np.linspace(100,200,len(self.dates))}, index=self.dates)
    def call(self, fetcher, info=None):
        return collect_yahoo(self.info if info is None else info,'United States',5,self.start,self.end,fetcher)
    def test_symbols(self):
        self.assertEqual(yahoo_symbol('BRK.B','United States'),'BRK-B')
        self.assertEqual(yahoo_symbol('7203','Japan'),'7203.T')
        with self.assertRaises(ValueError): yahoo_symbol('BDO','Philippines')
    def test_market_cutoff(self):
        # 22 UTC = 17 New York; current session still excluded conservatively.
        self.assertEqual(request_window('United States',5,datetime(2026,11,24,22,tzinfo=timezone.utc)),('2021-11-24','2026-11-24'))
        self.assertEqual(request_window('United States',8,datetime(2026,11,24,23,tzinfo=timezone.utc)),('2018-11-25','2026-11-25'))
        self.assertEqual(request_window('Japan',5,datetime(2026,11,24,9,tzinfo=timezone.utc))[1],'2026-11-25')
    def test_valid(self):
        p,m,a=self.call(lambda *args:(self.hist.copy(),'USD'))
        self.assertEqual(p.shape,(len(self.dates),2)); self.assertTrue(a.status.eq('Eligible').all())
        self.assertEqual(list(m.index),list(p.columns))
    def test_currency(self):
        p,_,a=self.call(lambda *args:(self.hist.copy(),'JPY'))
        self.assertTrue(p.empty); self.assertTrue(a.reason.str.contains('USD').all())
    def test_no_raw_substitution(self):
        p,_,a=self.call(lambda *args:(self.hist.rename(columns={'Adj Close':'Close'}),'USD'))
        self.assertTrue(p.empty); self.assertTrue(a.reason.str.contains('not substituted').all())
    def test_new_listing(self):
        p,_,a=self.call(lambda *args:(self.hist.iloc[300:].copy(),'USD'))
        self.assertTrue(p.empty); self.assertTrue(a.reason.str.contains('cover').all())
    def test_stale_history(self):
        p,_,a=self.call(lambda *args:(self.hist.iloc[:-30].copy(),'USD'))
        self.assertTrue(p.empty); self.assertTrue(a.reason.str.contains('behind').all())
    def test_gap_is_not_filled(self):
        def fetch(symbol,*_):
            return (self.hist.drop(self.dates[40]) if symbol=='MSFT' else self.hist.copy()),'USD'
        p,_,a=self.call(fetch)
        self.assertEqual(list(p.columns),['AAPL'])
        self.assertEqual(a.loc[a.ticker.eq('MSFT'),'status'].item(),'Excluded')
    def test_invalid_values_and_duplicates(self):
        for bad in [np.nan,0,np.inf,-1]:
            h=self.hist.copy();h.iloc[40,0]=bad
            p,_,_=self.call(lambda *args:(h,'USD'));self.assertTrue(p.empty)
        h=pd.concat([self.hist,self.hist.iloc[:1]])
        p,_,a=self.call(lambda *args:(h,'USD'));self.assertTrue(p.empty)
        self.assertTrue(a.reason.str.contains('Duplicate').all())
    def test_failure_circuit_and_safe_messages(self):
        calls=[]
        info=pd.concat([self.info]*3).reset_index(drop=True)
        info.index=[f'T{i}' for i in range(len(info))]
        def fail(symbol,*_):
            calls.append(symbol);raise RuntimeError('private_provider_error_body')
        p,_,a=self.call(fail,info)
        self.assertTrue(p.empty);self.assertEqual(len(calls),3)
        self.assertFalse(a.to_csv().find('private_provider_error_body')>=0)
        self.assertIn('Not requested',a.iloc[-1].reason)
    def test_rate_limit_stops_after_one_request(self):
        calls = []
        YFRateLimitError = type('YFRateLimitError', (RuntimeError,), {})
        def limited(symbol, *_):
            calls.append(symbol)
            raise YFRateLimitError('provider limit')
        p, _, audit = self.call(limited)
        self.assertTrue(p.empty)
        self.assertEqual(len(calls), 1)
        self.assertTrue(audit.iloc[1].reason.startswith('Not requested'))

    def test_failure_isolated_and_order_preserved(self):
        def fetch(symbol,*_):
            if symbol=='AAPL': raise RuntimeError('failure')
            return self.hist.copy(),'USD'
        p,m,a=self.call(fetch)
        self.assertEqual(list(p.columns),['MSFT']); self.assertEqual(m.company.item(),'Microsoft')
        self.assertEqual(a.status.tolist(),['Excluded','Eligible'])

if __name__=='__main__': unittest.main()
