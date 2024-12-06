class Constants:
    """
    A class to hold constant mappings and scales used throughout the application.

    Attributes
    ----------
    freq_map : dict
        A dictionary mapping time frequencies to their corresponding pandas resample codes.
        Keys are:
            'quarterly' -> 'Q'
            'monthly' -> 'M'
            'yearly' -> 'Y'
    agg_map : dict
        A dictionary mapping aggregation methods to their corresponding pandas aggregation functions.
        Keys are:
            'lastvalue' -> 'last'
            'mean' -> 'mean'
            'sum' -> 'sum'
            'min' -> 'min'
            'max' -> 'max'
    ANNSCALE_MAP : dict
        A dictionary mapping time frequencies to their corresponding annualization scales.
        Keys are:
            'daily' -> 36500
            'weekly' -> 5200
            'monthly' -> 1200
            'quarterly' -> 400
            'yearly' -> 100
            'annual' -> 100
    """
    # MATLAB retime map to pandas resample
    freq_map = {
        'hourly': 'H',
        'daily': 'D',
        'monthly': 'ME',
        'quarterly': 'QE-DEC',
        'yearly': 'YE',
        'H' : 'H',
        'D' : 'D',
        'M' : 'ME',
        'ME': 'ME',
        'Q' : 'QE-DEC',
        'QE': 'QE-DEC',
        'QE-DEC': 'QE-DEC',
        'Y' : 'YE-DEC',
        'YE': 'YE-DEC',
        'YE-DEC': 'YE-DEC',
    }
    freq_to_n = ['H', 'D', 'M', 'QE-DEC', 'Y']
    agg_map = {
        'lastvalue': 'last',
        'mean': 'mean',
        'sum': 'sum',
        'min': 'min',
        'max': 'max'
    }

    # Annualization scales
    ANNSCALE_MAP = {
        'daily': 36500,
        'weekly' : 5200,
        'monthly' : 1200,
        'quarterly' : 400,
        'yearly' : 100,
        "annual": 100,
        'D': 36500,
        'W': 5200,
        'M': 1200,
        'Q': 400,
        'QE': 400,
        'QE-DEC': 400,
        'Y': 100
    }

    # group similar date formats
    year_like = ['Y', 'YE', 'yearly', 'annual']
    quarter_like = ['Q', 'QE', 'QE-DEC', 'quarterly']
    month_like = ['M', 'ME', 'monthly']