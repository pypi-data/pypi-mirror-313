# import libraries
import unittest
import pandas as pd
from pandas.testing import assert_series_equal

# get Timeseries class
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..', 'src', 'macroecon_tools'))
from Data import Timeseries

class TestTimeseries(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.sample_data = pd.Series([i for i in range(24)], index=pd.date_range("2020-01-01", periods=24, freq="ME"))
        self.ts = Timeseries(self.sample_data, name="Sample", freq="monthly")

    def test_copy(self):
        ts_copy = self.ts.copy()
        # Assert that the copied instance is not the same as the original
        self.assertIsNot(ts_copy, self.ts)
        # Assert that the data and attributes of the copied instance are equal to the original
        self.assertTrue(ts_copy.equals(self.ts))
        self.assertEqual(ts_copy.name, self.ts.name)
        self.assertEqual(ts_copy.get_freqstr(), self.ts.get_freqstr())
        self.assertEqual(ts_copy.transformations, self.ts.transformations)

if __name__ == '__main__':
    unittest.main()