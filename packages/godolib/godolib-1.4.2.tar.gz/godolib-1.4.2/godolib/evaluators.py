import tensorflow as tf
import numpy as np


def r2(y_true, y_pred):
    """
    Computes the coefficient of determination (R^2) in a vectorized manner.

    The R^2 metric measures the proportion of variance in the target values 
    that is predictable from the features. It is computed for each feature 
    across all samples, averaged across features and samples.

    Parameters:
    ----------
    y_true : tf.Tensor
        Ground truth values with shape (batch_size, timesteps, features).
        Represents the true values for each timestep and feature.
    
    y_pred : tf.Tensor
        Predicted values with shape (batch_size, timesteps, features).
        Represents the model predictions for each timestep and feature.

    Returns:
    -------
    r2_average : tf.Tensor
        A scalar tensor representing the average R^2 score across all features 
        and samples. Higher values indicate better performance.
    
    Notes:
    -----
    - The R^2 score is defined as:
        R^2 = 1 - (SS_residual / SS_total)
      where:
        SS_residual = sum((y_true - y_pred) ** 2)
        SS_total = sum((y_true - mean(y_true)) ** 2)
    
    - This implementation avoids division by zero by replacing zero values in 
      SS_total with ones to maintain numerical stability.
    """
    # Compute the mean of y_true along the timestep axis for each feature
    y_true_mean = tf.reduce_mean(y_true, axis=1, keepdims=True)

    # Total sum of squares (SS_total): sum((y_true - mean(y_true)) ** 2)
    ss_total = tf.reduce_sum(tf.square(y_true - y_true_mean), axis=1)

    # Residual sum of squares (SS_residual): sum((y_true - y_pred) ** 2)
    ss_residual = tf.reduce_sum(tf.square(y_true - y_pred), axis=1)

    # Avoid division by zero in SS_total
    ss_total = tf.where(tf.equal(ss_total, 0), tf.ones_like(ss_total), ss_total)

    # Compute R^2 per sample and per feature
    r2_per_sample = 1 - (ss_residual / ss_total)

    # Average R^2 across all samples and features
    r2_average = tf.reduce_mean(r2_per_sample)
    
    return r2_average

def simple_r2(y_true, y_pred):
    """
    Calculate the coefficient of determination (R²) for a set of true and predicted values.

    The R² score, also known as the coefficient of determination, is a statistical measure that
    represents the proportion of the variance in the dependent variable that is predictable from 
    the independent variables. It is commonly used to evaluate the performance of regression models.

    Parameters:
    ----------
    y_true : array-like
        The true values or observed data. This can be a list, tuple, or numpy array.
        
    y_pred : array-like
        The predicted values from a model. This can be a list, tuple, or numpy array.

    Returns:
    -------
    r2 : float
        The R² score. A value of:
        - 1 indicates a perfect fit,
        - 0 indicates that the model predicts no better than the mean of `y_true`,
        - Negative values indicate a poor fit where the model performs worse than predicting the mean.

    Notes:
    -----
    - The function converts the inputs to numpy arrays internally to perform computations.
    - The calculation is based on the formula:
      R² = 1 - (SS_residual / SS_total)
      where:
        - SS_residual is the sum of squared residuals: Σ(y_true - y_pred)²
        - SS_total is the total sum of squares: Σ(y_true - mean(y_true))²

    Example:
    -------
    >>> import numpy as np
    >>> y_true = [3, -0.5, 2, 7]
    >>> y_pred = [2.5, 0.0, 2, 8]
    >>> simple_r2(y_true, y_pred)
    0.9486081370449679
    """
    
    ss_total = np.sum((y_true - np.mean(y_true))**2)
    ss_residual = np.sum((y_true - y_pred)**2)
    r2 = 1 - (ss_residual / ss_total)
    
    return r2
