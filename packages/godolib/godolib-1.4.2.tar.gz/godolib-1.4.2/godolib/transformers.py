from .fast_transformers import calculate_returns, calculate_inverse_returns, calculate_log_returns, calculate_inverse_log_returns, calculate_volatility_on_prices, window, inverse_window, standardize, inverse_standardize
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ZScoreCalculator(BaseEstimator, TransformerMixin):
    """
    A transformer class that standardizes data by calculating the z-score for each feature in a 2D array.
    Inherits from scikit-learn's BaseEstimator and TransformerMixin to allow integration into pipelines.

    Methods:
    --------
    fit(X, y=None):
        Calculates and stores the mean and standard deviation for each feature in the input array.
    
    transform(X, y=None):
        Applies z-score standardization to the input data using the stored mean and standard deviation.
    
    inverse_transform(X, y=None):
        Reverses the standardization process, returning the data to its original scale.

    Raises:
    -------
    ValueError:
        If X is not a 2D numpy array or contains NaN values.

    Attributes:
    -----------
    mean : ndarray
        The mean of each feature in the input array, calculated during fit.
    
    std : ndarray
        The standard deviation of each feature in the input array, calculated during fit.
    """
    
    def fit(self, X, y=None):
        """
        Calculates the mean and standard deviation of each feature in the input array X.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The input data to fit, which should be a 2D numpy array.
        
        y : None
            Ignored, not used in this method.

        Returns:
        --------
        self : ZScoreCalculator
            The fitted instance with stored mean and standard deviation.
        
        Raises:
        -------
        ValueError:
            If X is not a numpy array, is not bidimensional, or contains NaN values.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError('X must be an array')
        if X.ndim != 2:
            raise ValueError('Array must be bidimensional')
        if np.isnan(X).any():
            raise ValueError('Array contains NaNs')
        
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        return self

    def transform(self, X, y=None):
        """
        Transforms the input array X by applying z-score standardization.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The input data to transform, which should be a 2D numpy array.

        y : None
            Ignored, not used in this method.

        Returns:
        --------
        transformed_X : array-like of shape (n_samples, n_features)
            The standardized data, where each feature has been transformed using z-scores.
        """
        transformed_X = standardize(array=X, mean=self.mean, std=self.std)
        return transformed_X

    def inverse_transform(self, X, y=None):
        """
        Reverses the z-score standardization, returning data to its original scale.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The standardized data to inverse transform, which should be a 2D numpy array.

        y : None
            Ignored, not used in this method.

        Returns:
        --------
        transformed_X : array-like of shape (n_samples, n_features)
            The data in its original scale.
        """
        transformed_X = inverse_standardize(array=X, std=self.std, mean=self.mean)
        return transformed_X


class VolatilityCalculator(BaseEstimator, TransformerMixin):
    """
    A transformer to calculate rolling volatility from a time series data array.

    Parameters:
    - return_period (int): The period over which returns are calculated for volatility.
    - window_size (int): The window size for rolling volatility calculation.
    - return_method (str): The method used for calculating returns ('percentage' or 'logarithmic'). Default is 'percentage'.
    - min_period (int): Minimum number of periods required to calculate the volatility. Default is 2.
    - ddof (int, optional): 1 for sample and 0 for population

    Attributes:
    - initial_values (np.ndarray): Initial values of the input array up to `return_period`.
    """
    def __init__(self, return_period, window_size, return_method='percentage', min_period=2, ddof=0):
        """
        Initializes the VolatilityCalculator with parameters for return calculation.
        Raises ValueError if an invalid return method is provided.
        """
        valid_return_methods = ['percentage', 'logarithmic']
        if return_method not in valid_return_methods:
            raise ValueError(f'{return_method} not a valid return method. Choose from {valid_return_methods}')
        if window_size<=1:
            raise ValueError(f'Window size must be a positive integer greater than 1')
        if ddof not in [1, 0]:
            raise ValueError('ffod parameter must be 0 or 1')
        self.return_period = return_period
        self.window_size = window_size
        self.return_method = return_method
        self.min_period = min_period
        self.ddof=ddof

    def fit(self, X, y=None):
        """
        Validates the input array `X` and stores initial values for use in transformations.
        Checks that `X` is a 2D numpy array without NaNs.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError('X must be an array')
        if X.ndim != 2:
            raise ValueError('Array must be bidimensional')
        if np.isnan(X).any():
            raise ValueError('Array contains NaNs')
        return self

    def transform(self, X, y=None):
        """
        Calculates rolling volatility for the input array `X` based on the specified parameters.
        """
        transformed_X = calculate_volatility_on_prices(array=X,
                                                       return_period=self.return_period,
                                                       window_size=self.window_size,
                                                       return_method=self.return_method,
                                                       min_period=self.min_period,
                                                       ddof=self.ddof)
        return transformed_X


class ReturnsCalculator(BaseEstimator, TransformerMixin):
    """
    A transformer to calculate percentage returns from a time series data array.

    Parameters:
    - period (int): The period over which returns are calculated.

    Attributes:
    - initial_values (np.ndarray): Initial values of the input array up to `period`.
    """
    def __init__(self, period):
        """
        Initializes the ReturnsCalculator with the specified period.
        """
        self.period = period

    def fit(self, X, y=None):
        """
        Validates the input array `X` and stores initial values for use in inverse transformations.
        Checks that `X` is a 2D numpy array without NaNs.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError('X must be an array')
        if X.ndim != 2:
            raise ValueError('Array must be bidimensional')
        if np.isnan(X).any():
            raise ValueError('Array contains NaNs')
        self.initial_values = X[:self.period, :]
        return self

    def transform(self, X, y=None):
        """
        Calculates percentage returns for the input array `X` over the specified period.
        """
        transformed_X = calculate_returns(array=X, period=self.period)
        return transformed_X

    def inverse_transform(self, X, y=None):
        """
        Reconstructs the original array from percentage returns using initial values.
        """
        recovered_X = calculate_inverse_returns(array=X, period=self.period, initial_values=self.initial_values)
        return recovered_X


class LogReturnsCalculator(BaseEstimator, TransformerMixin):
    """
    A transformer to calculate logarithmic returns from a time series data array.

    Parameters:
    - period (int): The period over which logarithmic returns are calculated.

    Attributes:
    - initial_values (np.ndarray): Initial values of the input array up to `period`.
    """
    def __init__(self, period):
        """
        Initializes the LogReturnsCalculator with the specified period.
        """
        self.period = period

    def fit(self, X, y=None):
        """
        Validates the input array `X` and stores initial values for use in inverse transformations.
        Checks that `X` is a 2D numpy array without NaNs.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError('X must be an array')
        if X.ndim != 2:
            raise ValueError('Array must be bidimensional')
        if np.isnan(X).any():
            raise ValueError('Array contains NaNs')
        self.initial_values = X[:self.period, :]
        return self

    def transform(self, X, y=None):
        """
        Calculates logarithmic returns for the input array `X` over the specified period.
        """
        transformed_X = calculate_log_returns(array=X, period=self.period)
        return transformed_X

    def inverse_transform(self, X, y=None):
        """
        Reconstructs the original array from logarithmic returns using initial values.
        """
        recovered_X = calculate_inverse_log_returns(array=X, period=self.period, initial_values=self.initial_values)
        return recovered_X

class WindowTransformer(BaseEstimator, TransformerMixin):
    """
    A custom transformer that generates sliding windows of past and future values from a time series array.
    Useful for preparing input data for time series forecasting models.

    Parameters
    ----------
    n_past : int
        The number of past timestamps to include in each window.
    n_future : int
        The number of future timestamps to predict for each window.

    Methods
    -------
    fit(X, y=None)
        Validates the input array `X` and checks that it has sufficient data points for the specified window sizes.
    transform(X, y=None)
        Transforms the input array into sliding windows of past and future values.
    inverse_transform(Xt, y=None)
        Reconstructs the original time series from the transformed data (windowed sequences of past and future values).

    Raises
    ------
    ValueError
        - If `X` is not a NumPy ndarray.
        - If `X` is not 2-dimensional.
        - If `X` contains any NaN values.
        - If the shape of `X` is insufficient for `n_past` or `n_future`.

    Example
    -------
    >>> import numpy as np
    >>> from sklearn.pipeline import Pipeline
    >>> data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    >>> transformer = WindowTransformer(n_past=2, n_future=1)
    >>> transformer.fit(data)
    WindowTransformer(n_past=2, n_future=1)
    >>> X, Y = transformer.transform(data)
    >>> X
    array([[[1., 2.],
            [3., 4.]],
           [[3., 4.],
            [5., 6.]],
           [[5., 6.],
            [7., 8.]]])
    >>> Y
    array([[[5., 6.]],
           [[7., 8.]],
           [[9., 10.]]])
    >>> reconstructed = transformer.inverse_transform((X, Y))
    """

    def __init__(self, n_past, n_future):
        """
        Initialize the transformer with window sizes for past and future values.
        
        Parameters
        ----------
        n_past : int
            Number of past values to include in each input window.
        n_future : int
            Number of future values to predict for each window.
        """
        self.n_past = n_past
        self.n_future = n_future

    def fit(self, X, y=None):
        """
        Validates the input array `X`.
        
        Ensures `X` is a 2D array, contains no NaN values, and has a sufficient number of rows for the specified `n_past` and `n_future` values.
        
        Parameters
        ----------
        X : np.ndarray
            A 2D array of time series data to be validated.
        y : None
            Ignored, kept for compatibility with scikit-learn's API.
        
        Returns
        -------
        self : WindowTransformer
            The instance itself, ready for transformation.
        """
        if not isinstance(X, np.ndarray):
            raise ValueError('Input must be an array')
        if X.ndim != 2:
            raise ValueError('Array must be bidimensional')
        if np.isnan(X).any():
            raise ValueError('Array contains NaNs')
        if X.shape[0] <= self.n_past:
            raise ValueError('Input shape not big enough for given n_past')
        if X.shape[0] <= self.n_future:
            raise ValueError('Input shape not big enough for given n_future')
        return self

    def transform(self, X, y=None):
        """
        Transforms the input array into sliding windows of past and future values.
        
        Uses the `window` function to generate input (X) and target (Y) windows from the original array.
        
        Parameters
        ----------
        X : np.ndarray
            A 2D array of time series data to be transformed.
        y : None
            Ignored, kept for compatibility with scikit-learn's API.
        
        Returns
        -------
        tuple of np.ndarray
            (X, Y), where X contains windows of past values and Y contains windows of future values.
        """
        return window(array=X, n_past=self.n_past, n_future=self.n_future)

    def inverse_transform(self, Xt, y=None):
        """
        Reconstructs the original time series from windowed data.
        
        Uses the `inverse_window` function to approximate the original time series based on the input and target windows.
        
        Parameters
        ----------
        Xt : tuple of np.ndarray
            Tuple (X, Y) where X contains past windows and Y contains future windows.
        y : None
            Ignored, kept for compatibility with scikit-learn's API.
        
        Returns
        -------
        np.ndarray
            The reconstructed time series array.
        """
        X, Y = Xt
        return inverse_window(X=X, Y=Y)