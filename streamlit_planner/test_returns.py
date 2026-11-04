import unittest
import numpy as np
import pandas as pd
from core.returns import weekly_returns

class WeeklyReturnsTests(unittest.TestCase):
    def test_compounding_and_partial_week(self):
        dates=pd.bdate_range('2024-01-05',periods=18)
        prices=pd.DataFrame({'A':100*1.01**np.arange(18)},index=dates)
        result=weekly_returns(prices)
        self.assertEqual(len(result),3)
        np.testing.assert_allclose(result.A,1.01**5-1)
    def test_holiday_last_available_close(self):
        dates=pd.to_datetime(['2024-01-05','2024-01-11','2024-01-19','2024-01-26'])
        result=weekly_returns(pd.DataFrame({'A':[100,110,121,133.1]},index=dates))
        np.testing.assert_allclose(result.A,.1)
    def test_missing_week_not_bridged(self):
        dates=pd.to_datetime(['2024-01-05','2024-01-12','2024-01-26','2024-02-02'])
        result=weekly_returns(pd.DataFrame({'A':[100,110,121,133.1]},index=dates))
        self.assertEqual(len(result),2)
        np.testing.assert_allclose(result.A,.1)
if __name__=='__main__': unittest.main()
