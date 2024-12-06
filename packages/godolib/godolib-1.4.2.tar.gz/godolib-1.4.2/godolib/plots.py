import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

def plot_histograms_with_stats(data):
    """
    Plots histograms for each column in a given array or DataFrame, highlighting statistical metrics.

    This function generates a grid of histograms (3 per row) for each column in the input data. For each histogram:
    - The mean is displayed as a vertical dashed line.
    - Standard deviation intervals are displayed as dotted lines around the mean.
    - The furthest point from the mean is marked with a solid line.
    - Supports both DataFrame and NumPy array inputs, using column names if provided by a DataFrame.

    Parameters:
    -----------
    data : pd.DataFrame or np.ndarray
        The input data for which histograms will be generated. Each column in the data is plotted as a separate histogram.
        If a DataFrame is passed, column names are used in the plot titles. If a NumPy array is provided, generic column
        names ('Column 1', 'Column 2', etc.) are used.

    Returns:
    --------
    None
        This function does not return a value. It displays a grid of histogram plots.

    Notes:
    ------
    - For each column, the function calculates:
        - Mean: Displayed with a gold dashed line.
        - Standard deviation intervals: Displayed as light green dotted lines around the mean.
        - Furthest point: Marked with a red solid line, representing the data point furthest from the mean in units of standard deviation.
    - Unused subplots (if the number of columns is not a multiple of 3) are hidden.

    Example:
    --------
    >>> dataframe = pd.DataFrame(np.random.randn(1000, 5), columns=['Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5'])
    >>> plot_histograms_with_stats(dataframe)
    """
    
    # Si el input es un DataFrame, obtener los nombres de las columnas y convertirlo a array
    if isinstance(data, pd.DataFrame):
        column_names = data.columns
        data = data.values
    else:
        # Si es un array, usar nombres de columnas genéricos
        column_names = [f'Column {i+1}' for i in range(data.shape[1])]
    
    num_columns = 3  # Número de columnas en la cuadrícula
    num_plots = data.shape[1]
    num_rows = math.ceil(num_plots / num_columns)  # Número de filas necesarias

    # Crear figura con fondo oscuro
    plt.style.use('dark_background')
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_columns, figsize=(15, 5 * num_rows))
    axes = axes.flatten()  # Aplanar los ejes para facilitar la iteración

    # Generar los gráficos para cada columna
    for idx in range(num_plots):
        mean = np.mean(data, axis=0)[idx]
        std = np.std(data, axis=0)[idx]
        furthest_point = data[np.argmax(abs(data[:, idx] - mean))][idx]
        furthest_point_dev = abs(furthest_point - mean) / std

        # Histograma en cada subplot
        axes[idx].hist(data[:, idx], bins=50, color='cyan', edgecolor='white', alpha=0.7)
        axes[idx].axvline(x=mean, color='gold', linestyle='--', linewidth=2, label=f'Mean = {mean:.2f}')
        
        # Líneas de desviación estándar
        for i in range(1, math.ceil(furthest_point_dev) + 1):
            axes[idx].axvline(x=mean + i * std, color='lightgreen', linestyle=':', linewidth=1.5)
            axes[idx].axvline(x=mean - i * std, color='lightgreen', linestyle=':', linewidth=1.5)

        # Destacar el punto más lejano
        axes[idx].axvline(x=furthest_point, color='tomato', linestyle='-', linewidth=2, label=f'Furthest Point = {furthest_point:.2f}')

        # Formato del gráfico
        axes[idx].set_title(f'Histogram of {column_names[idx]}', color='white')
        axes[idx].set_xlabel('Values', color='white')
        axes[idx].set_ylabel('Frequency', color='white')
        axes[idx].legend(loc='upper right', facecolor='black', framealpha=0.9)
        axes[idx].grid(True, linestyle='--', alpha=0.4, color='gray')

    # Apagar subplots extra
    for idx in range(num_plots, len(axes)):
        axes[idx].axis('off')  # Ocultar ejes sobrantes

    plt.tight_layout()
    plt.show()
