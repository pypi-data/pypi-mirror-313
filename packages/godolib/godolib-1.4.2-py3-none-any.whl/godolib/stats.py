import numpy as np
from statsmodels.tsa.stattools import acf, pacf

def calculate_acf(array, lags):
    """
    Calculate the autocorrelation function (ACF) for a 2D array of time series data over a specified number of lags.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    lags : int
        The number of lags for which to compute the ACF for each time series.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array of shape (lags + 1, array.shape[1]), where each column contains the ACF values 
        for the corresponding time series across the specified lags.

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    This function computes the autocorrelation function (ACF) up to the specified number of lags for each time series 
    in the input array. It uses the `acf` function from the statsmodels library to calculate ACF values for each 
    individual time series, storing the results in `acf_array`.

    Example
    -------
    >>> import numpy as np
    >>> from statsmodels.tsa.stattools import acf
    >>> data = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]])
    >>> calculate_acf(data, lags=2)
    array([[1.        , 1.        ],
           [0.75      , 0.75      ],
           [0.5       , 0.5       ]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    acf_array = np.zeros(shape=(lags + 1, array.shape[1]))
    for layer in range(array.shape[1]):
        acf_array[:, layer] = acf(array[:, layer].reshape(-1, 1), nlags=lags)
    return acf_array

def calculate_pacf(array, lags):
    """
    Calculate the partial autocorrelation function (PACF) for a 2D array of time series data over a specified number of lags.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    lags : int
        The number of lags for which to compute the PACF for each time series.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array of shape (lags + 1, array.shape[1]), where each column contains the PACF values 
        for the corresponding time series across the specified lags.

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    This function computes the partial autocorrelation function (PACF) up to the specified number of lags for each 
    time series in the input array. It uses the `pacf` function from the statsmodels library to calculate PACF values 
    for each individual time series, storing the results in `pacf_array`.

    Example
    -------
    >>> import numpy as np
    >>> from statsmodels.tsa.stattools import pacf
    >>> data = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]])
    >>> calculate_pacf(data, lags=2)
    array([[1.        , 1.        ],
           [0.5       , 0.5       ],
           [0.        , 0.        ]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    pacf_array = np.zeros(shape=(lags + 1, array.shape[1]))
    for layer in range(array.shape[1]):
        pacf_array[:, layer] = pacf(array[:, layer].reshape(-1, 1), nlags=lags)
    return pacf_array
