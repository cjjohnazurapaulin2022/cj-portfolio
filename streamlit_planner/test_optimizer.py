"""Synthetic fixtures only; no real stock or performance claims."""
import unittest
from itertools import combinations
import numpy as np
from core.optimizer import optimize

class EngineTests(unittest.TestCase):
    def setUp(self):
        rng=np.random.default_rng(42)
        self.r=rng.normal(0,.01,(80,9))+np.arange(9)*.0002
        self.names=[f'TEST{i}' for i in range(9)]
        self.industries=['A']*3+['B']*3+['C']*3
    def run_model(self,**kw):
        return optimize(self.r,self.names,self.industries,['A','B','C'],**kw)
    def test_objectives_and_selection_exhaustively(self):
        mu=self.r.mean(0);mad=np.abs(self.r-mu).mean(0)
        for obj in ['return','risk','balanced']:
            out=self.run_model(objective=obj)
            ids=[self.names.index(x['ticker']) for x in out['allocation']]
            score=mu if obj=='return' else -mad if obj=='risk' else .5*(mu-mu.min())/np.ptp(mu)-.5*(mad-mad.min())/np.ptp(mad)
            best=max(sum(score[list(c)]) for c in combinations(range(9),5) if len({self.industries[i] for i in c})==3)
            self.assertAlmostEqual(sum(score[ids]),best,places=8)
            w=np.array([x['weight'] for x in out['allocation']])
            self.assertAlmostEqual(w.sum()+out['cash_weight'],1)
            self.assertEqual(len(ids),5)
            self.assertEqual(len({self.industries[i] for i in ids}),3)
            self.assertTrue(np.all(w>=.01-1e-7) and np.all(w<=.35+1e-7))
            self.assertAlmostEqual(out['daily_mad'],np.abs((self.r[:,ids]-mu[ids])@w).mean())
    def test_analytical_constant_return(self):
        r=np.tile([.01,.02,.03],(10,1))
        out=optimize(r,['A','B','C'],['A','B','C'],['A','B','C'],count=3,objective='return',maximum=.6)
        self.assertAlmostEqual(out['daily_return'],.01*.01+.02*.39+.03*.6,places=8)
    def test_risk_cash(self):
        r=np.tile([[-.01]*3,[.01]*3],(10,1))
        out=optimize(r,['A','B','C'],['A','B','C'],['A','B','C'],count=3,objective='risk')
        self.assertAlmostEqual(out['cash_weight'],.1,places=6)
        self.assertAlmostEqual(out['daily_mad'],.009,places=7)
    def test_fixed_reserve_all_objectives(self):
        for reserve in [0., .05, .10]:
            for objective in ['return', 'risk', 'balanced']:
                out=self.run_model(objective=objective, cash_reserve=reserve, capital=1000000)
                self.assertAlmostEqual(out['cash_amount'],1000000*reserve,places=6)
                self.assertAlmostEqual(sum(x['weight'] for x in out['allocation']),1-reserve)
                self.assertAlmostEqual(sum(x['amount'] for x in out['allocation'])+out['cash_amount'],1000000)
    def test_fixed_reserve_feasibility(self):
        for kw in [{'cash_reserve':.1,'minimum':.19},
                   {'cash_reserve':0.,'maximum':.19},
                   {'cash_reserve':.11}, {'cash_reserve':-.1}, {'cash_reserve':float('nan')}]:
            with self.assertRaises(ValueError): self.run_model(**kw)
        out=self.run_model(cash_reserve=.1,minimum=.18,maximum=.18)
        self.assertTrue(all(abs(x['weight']-.18)<1e-7 for x in out['allocation']))
    def test_invalid(self):
        for kw in [{'maximum':.15},{'count':10},{'minimum':.25},{'capital':0}]:
            with self.assertRaises(ValueError):self.run_model(**kw)
    def test_identical_and_scaling(self):
        a=self.run_model(capital=100);b=self.run_model(capital=1000)
        for x,y in zip(a['allocation'],b['allocation']):self.assertAlmostEqual(x['amount']*10,y['amount'])
        for obj in ['return','risk','balanced']:
            out=optimize(np.zeros((10,3)),['A','B','C'],['A','B','C'],['A','B','C'],count=3,objective=obj)
            self.assertEqual(out['daily_mad'],0)
if __name__=='__main__':unittest.main(verbosity=2)
