# Load packages
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

# system imports
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# package imports
from constants import Constants
from Data import Timeseries

def gen_moment_func(moment: str):
    """
    Returns a function to compute the specified statistical moment.

    Parameters
    ----------
    moment : str
        The statistical moment to compute. Options are 'mean', 'SD', 'Skew', 'Kurt', 'min', 'max'.

    Returns
    -------
    function
        A function that computes the specified moment on an array-like input.

    Raises
    ------
    ValueError
        If the specified moment is not available.
    """
    if moment == 'mean':
        return lambda X: np.nanmean(X, axis=0)
    elif moment == 'SD':
        return lambda X: np.nanstd(X, axis=0, ddof=1)
    elif moment == 'Skew':
        return lambda X: skew(X, axis=0, nan_policy='omit', bias=False)
    elif moment == 'Kurt':
        return lambda X: kurtosis(X, axis=0, nan_policy='omit', bias=False)
    elif moment == 'min':
        return lambda X: np.nanmin(X, axis=0)
    elif moment == 'max':
        return lambda X: np.nanmax(X, axis=0)
    else:
        raise ValueError('Moment not available')

def data_moments(data, vars: list[str], moments: list[str]):
    """
    Computes specified statistical moments for given variables in a dataset.

    Parameters
    ----------
    data : pd.DataFrame
        The dataset containing the variables.
    vars : list of str
        The list of variable names for which to display the moments.
    moments : list of str
        The list of moments to compute. Options are 'mean', 'SD', 'Skew', 'Kurt', 'min', 'max'.

    Returns
    -------
    None
        Prints the table of computed moments for the specified variables.
    """
    # Create empty table
    moments_table = pd.DataFrame()

    # Compute moments and append to table
    for imom in range(len(moments)):
        stat_function = gen_moment_func(moments[imom])
        # apply each fun to the columns 
        vals = []
        for col in data.columns:
            vals.append(stat_function(data[col]))
        # append vals as a new row to momtab
        moments_table = pd.concat([moments_table, pd.DataFrame([vals])], ignore_index=True)
    
    # Round and add row labels
    def format_numbers(x):
        return f"{x:.3f}"
    moments_table = moments_table.applymap(format_numbers)
    moments_table.columns = data.columns
    moments_table.index = moments

    # Display table
    print(moments_table[vars])