import itertools
import unittest
import numpy as np
import pandas as pd
from core.optimizer import optimize
from core.stock_insights import stock_insights

class StockInsightTests(unittest.TestCase):
    def setUp(self):
        self.tickers=['A1','A2','B1','B2','C1','C2']
        self.industries=['A','A','B','B','C','C']
        self.weekly=pd.DataFrame([
            [.01,.02,-.01,.03,.005,0],
            [.02,.00,.00,-.01,.015,.01],
            [-.01,.01,.02,.02,.01,-.01],
            [.00,.03,-.01,.00,0,.02],
        ],index=pd.date_range('2026-01-09',periods=4,freq='W-FRI'),columns=self.tickers)
    def run_case(self,objective,preference=.5,limit=None):
        result=optimize(self.weekly,self.tickers,self.industries,['A','B','C'],
                        count=3,minimum=.01,maximum=.4,cash_reserve=.1,
                        objective=objective,preference=preference,stock_risk_limit=limit)
        return result,stock_insights(self.weekly,self.tickers,self.industries,['A','B','C'],
                                    result,objective,preference,limit)
    def test_selection_scores_explain_actual_optimum(self):
        r=self.weekly.to_numpy();mu=r.mean(axis=0);mad=np.abs(r-mu).mean(axis=0)
        for objective,pref in [('return',.5),('risk',.5),('balanced',.3),('balanced',0),('balanced',1)]:
            result,(e,_,_)=self.run_case(objective,pref)
            if objective=='return':score=mu
            elif objective=='risk':score=-mad
            else:score=pref*(mu-mu.min())/np.ptp(mu)-(1-pref)*(mad-mad.min())/np.ptp(mad)
            valid=[combo for combo in itertools.combinations(range(6),3)
                   if {self.industries[i] for i in combo}=={'A','B','C'}]
            best=max(score[list(c)].sum() for c in valid)
            self.assertAlmostEqual(e.score.sum(),best,places=9)
            for ticker in e.index:self.assertAlmostEqual(e.loc[ticker,'score'],score[self.tickers.index(ticker)])
    def test_stock_metrics_and_chart_agree_with_price_ratios(self):
        _,(_,performance,chart)=self.run_case('return')
        # Reconstruct prices independently by iterated multiplication.
        for ticker in chart.columns:
            prices=[100.]
            for value in self.weekly[ticker]:prices.append(prices[-1]*(1+value))
            np.testing.assert_allclose(chart[ticker],prices)
            self.assertAlmostEqual(performance.loc[ticker,'Cumulative return (%)'],100*(prices[-1]/prices[0]-1))
            self.assertAlmostEqual(performance.loc[ticker,'Average weekly return (%)'],100*sum(self.weekly[ticker])/4)
        self.assertTrue(chart.iloc[0].eq(100).all())
        self.assertEqual(chart.index[0],self.weekly.index[0]-pd.Timedelta(days=7))
        self.assertEqual(chart.index[-1],self.weekly.index[-1])
        self.assertNotIn('CASH',chart.columns)
    def test_rank_and_risk_filter_use_eligible_candidates(self):
        result,(e,_,_)=self.run_case('return',limit=.018)
        eligible=self.weekly.std(ddof=1).le(.018)
        for ticker in e.index:
            ind=self.industries[self.tickers.index(ticker)]
            peers=[t for t,s in zip(self.tickers,self.industries) if s==ind and eligible[t]]
            rank=1+sum(self.weekly[t].mean()>self.weekly[ticker].mean() for t in peers)
            self.assertEqual(e.loc[ticker,'industry_count'],len(peers))
            self.assertEqual(e.loc[ticker,'industry_rank'],rank)
        self.assertEqual(result['candidate_count'],sum(eligible))
    def test_equal_scores_share_rank(self):
        w=self.weekly*0+.01
        result=optimize(w,self.tickers,self.industries,['A','B','C'],count=3,maximum=.4,cash_reserve=.1)
        e,performance,_=stock_insights(w,self.tickers,self.industries,['A','B','C'],result,'balanced')
        self.assertTrue(e.industry_rank.eq(1).all())
        self.assertTrue(e.score.eq(0).all())
        np.testing.assert_allclose(performance['Weekly MAD (%)'],0,atol=1e-12)

if __name__=='__main__':unittest.main()
