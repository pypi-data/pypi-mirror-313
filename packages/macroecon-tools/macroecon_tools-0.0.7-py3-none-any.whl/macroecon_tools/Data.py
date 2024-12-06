# Description: A class used to represent a timeseries object.

# Import libraries
import pandas as pd
import numpy as np
from scipy.signal import detrend
from datetime import datetime
from dateutil.relativedelta import relativedelta
import quantecon as qe

# Add path to constants
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import constants
from constants import Constants

class TimeseriesDF(pd.DataFrame):
    """
    A DataFrame that uses Timeseries for its columns.
    """
    @property
    def _constructor(self):
        return TimeseriesDF

    @property
    def _constructor_sliced(self):
        return Timeseries
    
    def __getitem__(self, key):
        result = super().__getitem__(key)
        if isinstance(result, pd.Series):
            result = Timeseries(result, name=result.name, freq=self.freq, transformations=[])
        return result
     

class Timeseries(pd.Series):
    """
    A class used to represent a timeseries object.

    Attributes
    ----------
    data : pd.Series
        a single variable in a time table
    freq : str
        the frequency of that variable
    variable_name : str
        the name of the variable

    Methods
    -------
    trans(form, lags=None)
        Transforms the data using the specified form (e.g., 'logdiff', 'diff', 'log', '100log').
        Must provide number of lags for 'logdiff' and 'diff'.
    agg(timestep, method)
        Aggregates the data using the specified method (e.g., 'quarterly', 'monthly', 'yearly').
        Must provide method (e.g., lastvalue, mean, sum).
    filter(method, date_one, date_two, p=None, h=None)
        Filters the data using the specified method (e.g., 'linear' or 'hamilton').
        Must provide start date (date_one) and end date (date_two).
        For 'hamilton', must also provide lag length (p) and lead length (h).
    """

    def __init__(self, data, name: str = None, freq: str = None, transformations: list[str] = [], *args, **kwargs):
        """
        Initializes a Timeseries object.

        Parameters
        ----------
        data : pd.Series or array-like
            a single variable in a time table
        name : str
            the name of the variable
        freq : str
            the frequency of that variable (e.g., 'quarterly', 'monthly', 'yearly')
        transformations : list[str]
            a list of transformations applied to the data
        
        Raises
        ------
        ValueError
            If frequency or variable name is not provided
        """
        # Call pd.Series constructor
        super().__init__(data, *args, **kwargs)

        # Track transformations
        self.transformations = transformations

        # Ensure the index is a datetime index
        try:
            self.index = pd.to_datetime(self.index)
        except:
            raise ValueError('Timeseries Class: Index must be a datetime index')

        # Check if need to rename
        if name:
            self.name = name
        if not self.name:
            raise ValueError('Timeseries Class: Variable name not provided')

        # Check for frequency
        if freq: # reindex to freq
            # self.reindex() # reindex to daily frequency 
            # self.index = pd.date_range(start=self.index[0], periods=len(self.index), freq=Constants.freq_map[freq])
            # self.transformations.append(f'reindex_{freq}')
            self.freq = Constants.freq_map[freq]
        elif not self.index.freq or not self.index.freqstr:
            raise ValueError('Timeseries Class: Frequency not provided')

    # getters
    def get_freqstr(self):
        """
        Returns the frequency of the timeseries.

        Returns
        -------
        str
            The frequency of the timeseries.
        """
        return self.index.freqstr
    
    # override string representation
    def __repr__(self):
        """
        Returns a string representation of the Timeseries object.

        Returns
        -------
        str
            A string representation of the Timeseries object.
        """
        # get size to display
        n = 5 if len(self) > 10 else int(len(self) / 2)
        # get the first 5 rows without the header
        start_data = ""
        for i in range(n):
            start_data += f"{self.index[i].strftime('%Y-%m-%d')}    {self.iloc[i]}\n"
        # get the last 5 rows
        end_data = ""
        for i in range(len(self) - n, len(self)):
            end_data += f"{self.index[i].strftime('%Y-%m-%d')}    {self.iloc[i]}\n"

        # return string
        return (f"{start_data}"
                f"\t...\n"
                f"{end_data}"
                f"...\n"
                f"Name: {self.name}, Freq: {self.get_freqstr()}, dtype: {self.dtype}\n"
                f"Transformations: {self.transformations}")    
 
    # Transform data
    def logdiff(self, nlag: int, freq: str = None):
        """
        Transforms the data using the log difference method.

        Parameters
        ----------
        nlag : int
            The lag length for the transformation.
        freq : str, optional
            Frequency of original data. Default is None.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        original_freq = self.get_freqstr() if not freq else freq
        annpp = Constants.ANNSCALE_MAP[original_freq] / nlag
        self = Timeseries(annpp * np.log(self / self.shift(nlag)), name=self.name, freq=original_freq, transformations=self.transformations)
        self.transformations.append('logdiff')
        return self
    
    def diff(self, nlag: int):
        """
        Transforms the data using the difference method.

        Parameters
        ----------
        nlag : int
            The lag length for the transformation.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        self = Timeseries(self - self.shift(nlag), name=self.name, freq=self.get_freqstr(), transformations=self.transformations)
        self.transformations.append(f'diff_{nlag}')
        return self
    
    def log(self):
        """
        Transforms the data using the log method.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        self = Timeseries(np.log(self), name=self.name, freq=self.get_freqstr(), transformations=self.transformations)
        self.transformations.append('log')
        return self
    
    def log100(self):
        """
        Transforms the data using the 100 times log method.

        Returns
        -------
        Timeseries
            A new Timeseries object with the transformed data.
        """
        self = Timeseries(100 * np.log(self), name=self.name, freq=self.get_freqstr(), transformations=self.transformations)
        self.transformations.append('log100')
        return self
    
    # Aggregation
    def agg(self, timestep: str, method: str):
        """
        Aggregates the data using the specified method.

        Parameters
        ----------
        timestep : str
            The timestep to aggregate the data (e.g., 'quarterly', 'monthly', 'yearly').
        method : str
            The aggregation method to use (e.g., 'lastvalue', 'mean', 'sum').

        Returns
        -------
        Timeseries
            A new Timeseries object with the aggregated data.
        """
        # Perform aggregation using super().agg
        aggregated = super().resample(Constants.freq_map[timestep]).agg(Constants.agg_map[method])
        # remove na
        aggregated = aggregated.dropna()
        # Create a new Timeseries object with the aggregated data
        self = Timeseries(aggregated, name=self.name, freq=Constants.freq_map[timestep], transformations=self.transformations)
        # Update transformations
        self.transformations.append(f'agg_{method}_{timestep}')
        return self
    
    # Resample
    def custom_reindex(self, freq: str ='D'):
        """
        Reindexes the data to daily frequency.

        Parameters
        ----------
        freq : str
            The frequency to resample the data (e.g., 'Q', 'M', 'Y' or 'quarterly', 'monthly', 'yearly').

        Returns
        -------
        None

        Notes
        -----
        This method modifies the Timeseries object in place.
        """
        # check if freq is in freq_map
        if freq in Constants.freq_map:
            freq = Constants.freq_map[freq]
        # reindex to daily frequency
        resampled = self.resample(freq).asfreq()
        self.update(resampled)
        self.transformations.append(f'reindex_{freq}')

    # Trunctate
    def trunc(self, date_one: str, date_two: str):
        """
        Truncates the data between the specified dates.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.

        Returns
        -------
        Timeseries
            A new Timeseries object with the truncated data.
        """
        # update self data
        self = Timeseries(self[date_one: date_two], name=self.name, freq=self.get_freqstr(), transformations=self.transformations)
        return self
    
    def copy_trunc(self, date_one: str, date_two: str):
        """
        Truncates the data between the specified dates.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.

        Returns
        -------
        Timeseries
            A new Timeseries object with the truncated data.
        """
        # update self data
        return Timeseries(self[date_one: date_two], name=self.name, freq=self.get_freqstr(), transformations=self.transformations)
    
    # filters
    def linear_filter(self, date_one: str, date_two: str):
        """
        Filters the data using the linear method.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.

        Returns
        -------
        Timeseries
            A new Timeseries object with the filtered data.
        """
        date_one = datetime.strptime(date_one, '%d-%b-%Y')
        date_two = datetime.strptime(date_two, '%d-%b-%Y')

        # Time range
        self = self.trunc(date_one, date_two)
        self = Timeseries(detrend(self, axis=0, type='linear'), name=self.name, freq=self.get_freqstr(), transformations=self.transformations)
        return self
    
    def hamilton_filter(self, date_one: str, date_two: str, lag_len: int = None, lead_len: int = None):
        """
        Filters the data using the Hamilton method.

        Parameters
        ----------
        date_one : str
            The start date in the format 'dd-mmm-yyyy'.
        date_two : str
            The end date in the format 'dd-mmm-yyyy'.
        lagLength : int, optional
            The lag length for the 'hamilton' filter. Default is None.
        leadLength : int, optional
            The lead length for the 'hamilton' filter. Default is None.

        Returns
        -------
        Timeseries
            A new Timeseries object with the filtered data.

        Raises
        ------
        ValueError
            If the frequency is not supported for the 'hamilton' filter.
        """
        date_one = datetime.strptime(date_one, '%d-%b-%Y')
        date_two = datetime.strptime(date_two, '%d-%b-%Y')

        # get default lag and lead lengths
        if self.get_freqstr() in Constants.year_like:
            lag_len = 1
            lead_len = 2
        elif self.get_freqstr() in Constants.quarter_like:
            lag_len = 4
            lead_len = 8
        elif self.get_freqstr() == Constants.month_like:
            lag_len = 12
            lead_len = 24
        else:
            raise ValueError(f'{self.get_freqstr()} frequency not supported for Hamilton filter')
        
        # get the tstart 
        if self.get_freqstr() in Constants.year_like:
            tstart = date_one - relativedelta(years=(lag_len + lead_len - 1))
        elif self.get_freqstr() in Constants.quarter_like:
            tstart = date_one - relativedelta(months=3*(lag_len + lead_len - 1))
        elif self.get_freqstr() in Constants.month_like:
            tstart = date_one - relativedelta(months=(lag_len + lead_len - 1))
        trham = self.copy_trunc(tstart, date_two)
        # Get cyclical component 
        cycle, trend = qe._filter.hamilton_filter(trham, lead_len, lag_len)
        cycle_series = pd.Series(cycle.flatten(), index=trham.index).dropna()
        self = Timeseries(cycle_series, name=self.name, freq=self.get_freqstr(), transformations=self.transformations)
        return self

if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.Series([1, 2, 3, 4], index=pd.date_range("2020-01-01", periods=4, freq="ME"))
    ts = Timeseries(sample_data, name="Sample", freq="monthly")
    print(ts)