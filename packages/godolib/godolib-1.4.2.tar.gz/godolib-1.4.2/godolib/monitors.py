from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf, adfuller, kpss
import matplotlib.pyplot as plt
from .preprocessing import ROCCalculator
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.callbacks import EarlyStopping


class TrainingSessionManager:
    """
    A class to manage training sessions across multiple configurations and trials.
    
    Attributes:
        executions_per_configuration (int): 
            Number of trials to run for each hyperparameter configuration.
        configurations (list): 
            A list of dictionaries representing hyperparameter configurations.
        building_func (callable): 
            A function that takes a hyperparameter configuration and returns a compiled model.
    """
    
    def __init__(self, executions_per_configuration, configurations, building_func):
        """
        Initializes the TrainingSessionManager with the required parameters.
        
        Parameters:
            executions_per_configuration (int): Number of trials to execute per configuration.
            configurations (list): List of hyperparameter configurations.
            building_func (callable): Function to build models using hyperparameter configurations.
        """
        self.executions_per_configuration = executions_per_configuration
        self.configurations = configurations
        self.building_func = building_func

    def global_train(self, X, Y, epochs, batch_size, validation_data, patience, verbose, metric='val_r2', mode='max'):
        """
        Conducts training sessions across all configurations and trials without rolling windows.
        
        Parameters:
            X (array-like): Training input data.
            Y (array-like): Training output data.
            epochs (int): Number of epochs to train.
            batch_size (int): Batch size for training.
            validation_data (tuple): Validation data as a tuple (X_val, Y_val).
            patience (int): Number of epochs with no improvement to wait before stopping early.
            verbose (int): Verbosity level for training.
            metric (str): Metric to monitor for early stopping. Defaults to 'val_r2'.
            mode (str): One of {'min', 'max'}. Defines whether the monitored metric should be minimized or maximized. Defaults to 'max'.
        
        Returns:
            pd.DataFrame: Consolidated results of all configurations and trials.
        """
        results = []
        print('Searching: ')
        for configuration_idx, configuration in enumerate(self.configurations):
            print(f'configuration: {configuration_idx}')
            configuration_results = []
            for trial in range(self.executions_per_configuration):
                print(f'trial: {trial}')
                model = self.building_func(HyperparametersSelector(configuration))
                current_callbacks = [EarlyStopping(monitor=metric, patience=patience, mode=mode)]
                trial_history = model.fit(
                    x=X, y=Y, batch_size=batch_size, epochs=epochs, verbose=verbose,
                    callbacks=current_callbacks, validation_data=validation_data
                )
                configuration_results.append(pd.DataFrame(trial_history.history))
            results.append(configuration_results)
        results = self._global_redistribute_(results)
        return results

    def rolling_train(self, X, Y, epochs, batch_size, validation_data, patience, verbose, metric='val_r2', mode='max'):
        """
        Conducts training sessions across all configurations and trials with rolling windows.
        
        Parameters:
            X (array-like): Training input data, structured for rolling windows.
            Y (array-like): Training output data, structured for rolling windows.
            epochs (int): Number of epochs to train.
            batch_size (int): Batch size for training.
            validation_data (tuple): Validation data as a tuple (X_val, Y_val) for rolling windows.
            patience (int): Number of epochs with no improvement to wait before stopping early.
            verbose (int): Verbosity level for training.
            metric (str): Metric to monitor for early stopping. Defaults to 'val_r2'.
            mode (str): One of {'min', 'max'}. Defines whether the monitored metric should be minimized or maximized. Defaults to 'max'.
        
        Returns:
            pd.DataFrame: Consolidated results of all configurations, trials, and windows.
        """
        results = []
        print('Searching: ')
        for configuration_idx, configuration in enumerate(self.configurations):
            print(f'configuration: {configuration_idx}')
            configuration_results = []
            for trial in range(self.executions_per_configuration):
                print(f'trial: {trial}')
                trial_results = []
                for window in range(X.shape[3]):
                    print(f'window: {window + 1}/{X.shape[3]}')
                    model = self.building_func(HyperparametersSelector(configuration))
                    current_callbacks = [EarlyStopping(monitor=metric, patience=patience, mode=mode)]
                    window_history = model.fit(
                        x=X[..., window], y=Y[..., window], batch_size=batch_size, epochs=epochs, verbose=verbose,
                        callbacks=current_callbacks,
                        validation_data=(validation_data[0][..., window], validation_data[1][..., window])
                    )
                    trial_results.append(pd.DataFrame(window_history.history))
                configuration_results.append(trial_results)
            results.append(configuration_results)
        results = self._rolling_redistribute_(results)
        return results

    def _global_redistribute_(self, results):
        """
        Restructures global training results into a DataFrame.
        
        Parameters:
            results (list): Results from global training organized by configuration and trial.
        
        Returns:
            pd.DataFrame: Restructured results with columns:
                - Configuration: Index of the hyperparameter configuration.
                - Trial: Index of the trial.
                - Epoch: Epoch number.
                - Metric: Metric name (e.g., loss, accuracy).
                - Value: Metric value.
        """
        redistributed_results = []
        for configuration_idx, configuration_results in enumerate(results):
            for trial_idx, trial_results in enumerate(configuration_results):
                for epoch in range(trial_results.shape[0]):
                    for metric in range(trial_results.shape[1]):
                        redistributed_results.append({
                            'Configuration': configuration_idx,
                            'Trial': trial_idx,
                            'Epoch': epoch,
                            'Metric': trial_results.columns[metric],
                            'Value': trial_results.iat[epoch, metric]
                        })
        return pd.DataFrame(redistributed_results)

    def _rolling_redistribute_(self, results):
        """
        Restructures rolling training results into a DataFrame.
        
        Parameters:
            results (list): Results from rolling training organized by configuration, trial, and window.
        
        Returns:
            pd.DataFrame: Restructured results with columns:
                - Configuration: Index of the hyperparameter configuration.
                - Trial: Index of the trial.
                - Window: Index of the rolling window.
                - Epoch: Epoch number.
                - Metric: Metric name (e.g., loss, accuracy).
                - Value: Metric value.
        """
        redistributed_results = []
        for configuration_idx, configuration_results in enumerate(results):
            for trial_idx, trial_results in enumerate(configuration_results):
                for window_idx, window_results in enumerate(trial_results):
                    for epoch in range(window_results.shape[0]):
                        for metric in range(window_results.shape[1]):
                            redistributed_results.append({
                                'Configuration': configuration_idx,
                                'Trial': trial_idx,
                                'Window': window_idx,
                                'Epoch': epoch,
                                'Metric': window_results.columns[metric],
                                'Value': window_results.iat[epoch, metric]
                            })
        return pd.DataFrame(redistributed_results)



class ModelManager ():
    """
    A class designed to manage the process of forecasting, backtesting, and plotting for time series models 
    with pre- and post-transformation pipelines. The class supports multi-step forecasting and backtesting 
    for both transformed and recovered data.

    Attributes:
    -----------
    post_transformation_pipeline : Pipeline
        The transformation pipeline applied after the returns calculation (e.g., standardization, windowing).
    transformation_pipeline : Pipeline
        The transformation pipeline applied to the raw data (e.g., differencing, scaling).
    transformed_df : pd.DataFrame
        The transformed time series data.
    recovered_df : pd.DataFrame
        The original time series data recovered from the transformation pipeline.
    model : Any
        The machine learning model used for forecasting.
    data_freq : str, optional (default='D')
        The frequency of the data, 'D' for daily and 'B' for business days.
    """
    def __init__ (self, post_transformation_pipeline, transformation_pipeline, transformed_df, model):
        """
        Initializes the ModelManager class with the given transformation pipelines, model, and data.

        Parameters:
        -----------
        post_transformation_pipeline : Pipeline
            Pipeline applied after the returns calculation (e.g., standardization, windowing).
        transformation_pipeline : Pipeline
            Pipeline applied to the raw data (e.g., differencing, scaling).
        transformed_df : pd.DataFrame
            Transformed time series data.
        model : Any
            The forecasting model.
        """
        self.post_transformation_pipeline = post_transformation_pipeline
        self.transformation_pipeline = transformation_pipeline
        self.transformed_df = transformed_df
        self.recovered_df = transformation_pipeline.inverse_transform(transformed_df)
        self.model = model
        plt.style.use('dark_background')
    def forecast (self, iterations = 5, data_freq = 'B', full_df = False, state='transformed'):
        """
        Generates a forecast for a given number of iterations into the future.

        Parameters:
        -----------
        iterations : int, optional (default=5)
            Number of steps to forecast into the future.
        data_freq : str, optional (default='B')
            The frequency of the predicted data ('B' for business days).
        full_df : bool, optional (default=False)
            If True, returns the full DataFrame of predictions, otherwise only the last 'iterations' rows.
        state : str, optional (default='transformed')
            Determines whether to return predictions in the 'transformed' or 'recovered' state.
        data_freq : str, optional (default='D')
            Data frequency, such as 'D' for daily or 'B' for business days.

        Returns:
        --------
        pd.DataFrame
            DataFrame of forecasted values either in the 'transformed' or 'recovered' state.
        """
        if iterations <= 0:
            raise ValueError(f'Must input positive iterations')
        valid_states = ['transformed', 'recovered']
        if state not in valid_states:
            raise ValueError(f"'{state}' is not a valid mode. Choose from {valid_states}.")
        full_transformed_future_df = self._forecast_(transformed_df = self.transformed_df, iterations = iterations)
        if state == 'transformed':
            transformed_dates = self._generate_dates_(state=state, df = full_transformed_future_df, data_freq=data_freq)
            full_transformed_future_df.index = transformed_dates
            if full_df:
                return full_transformed_future_df
            return full_transformed_future_df.iloc[-iterations:, :]
        elif state == 'recovered':
            full_recovered_future_df = self.transformation_pipeline.inverse_transform(full_transformed_future_df)
            recovered_dates = self._generate_dates_(state=state, df=full_recovered_future_df, data_freq=data_freq)
            full_recovered_future_df.index = recovered_dates
            if full_df:
                return full_recovered_future_df
            return full_recovered_future_df.iloc[-iterations:, :]
    def back_test (self, roll_size = 5, state = 'transformed'):
        """
        Performs a backtest over the last 'roll_size' time steps, comparing observed and predicted values.

        Parameters:
        -----------
        roll_size : int, optional (default=5)
            Number of steps used for the backtest.
        state : str, optional (default='transformed')
            Determines whether to perform backtesting on 'transformed' or 'recovered' data.

        Returns:
        --------
        Tuple[pd.DataFrame, pd.DataFrame]
            A tuple containing the observed and predicted DataFrames for the backtest period.
        """
        valid_states = ['transformed', 'recovered']
        if state not in valid_states:
            raise ValueError(f"'{state}' is not a valid mode. Choose from {valid_states}.")
        to_forecast_df = self.transformed_df.iloc[:-roll_size, :].copy()
        full_predicted_df = self._forecast_(transformed_df = to_forecast_df, iterations = roll_size)
        if state == 'transformed':
            observed_df = self.transformed_df.iloc[-roll_size - 1:, :]
            predicted_df = full_predicted_df.iloc[-roll_size - 1:, :]
            predicted_df.index = observed_df.index
            return observed_df, predicted_df
        elif state == 'recovered':
            observed_df = self.recovered_df.iloc[-roll_size - 1:, :]
            full_predicted_recovered_df = self.transformation_pipeline.inverse_transform(full_predicted_df)
            predicted_recovered_df = full_predicted_recovered_df.iloc[-roll_size - 1:, :]
            return observed_df, predicted_recovered_df

    def plot_forecast(self, features, iterations, data_freq='B', state='transformed', x_size=5, backend='matplotlib', palette='cool'):
        """
        Plots the forecasted and observed data for the specified features using either Matplotlib or Plotly.

        Parameters:
        -----------
        features : list[int or str]
            Features to plot (either column indices or names).
        iterations : int
            Number of steps to forecast into the future.
        data_freq : str, optional (default='B')
            The frequency of the predicted data ('B' for business days).
        state : str, optional (default='transformed')
            Determines whether to plot data in the 'transformed' or 'recovered' state.
        x_size : int, optional (default=5)
            Number of past steps to display in the plot.
        backend : str, optional (default='matplotlib')
            The plotting backend ('matplotlib' or 'plotly').
        palette : str, optional (default='cool')
            Color palette for the plot.
        """
        valid_backends = ['matplotlib', 'plotly']
        if backend not in valid_backends:
            raise ValueError(f"'{backend}' is not a valid mode. Choose from {valid_backends}.")
        valid_states = ['transformed', 'recovered']
        if state not in valid_states:
            raise ValueError(f"'{state}' is not a valid mode. Choose from {valid_states}.")
        
        future_df = self.forecast(iterations=iterations, data_freq=data_freq, state=state)
        
        if state == 'transformed':
            last_observed = self.transformed_df.iloc[-x_size:, :]
        elif state == 'recovered':
            last_observed = self.recovered_df.iloc[-x_size:, :]
        
        if isinstance(features, (str, int)):
            features = [features]

        features = [self.recovered_df.columns.tolist().index(feature) if isinstance(feature, str) else feature for feature in features]
        future_df = pd.concat([last_observed.iloc[-1:, :], future_df], axis=0)
        if backend == 'matplotlib':
            plt.figure(figsize=(12, 6), facecolor='black')
            cmap = plt.colormaps[palette]
            colors = cmap(np.linspace(0, 1, len(features)))  
            for idx, feature in enumerate(features):
                plt.plot(
                    last_observed.index, last_observed.values[:, feature], 
                    label=f'Observed {last_observed.columns[feature]}', 
                    color=colors[idx], linewidth=2
                )
                plt.plot(
                    future_df.index, future_df.values[:, feature], 
                    linestyle='--', label=f'Predicted {last_observed.columns[feature]}', 
                    color=colors[idx], linewidth=2
                )
            plt.title(f'Forecast', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Feature Value', fontsize=14)
            plt.legend(loc='upper left', fontsize=12, frameon=True, fancybox=True, framealpha=0.7)
            plt.grid(True, which='both', linestyle=':', linewidth=0.5, color='gray')
            plt.tight_layout()
            plt.show()
            
        elif backend == 'plotly':
            traces = []
            colors = px.colors.qualitative.Plotly
            for i, feature in enumerate(features):
                traces.append(go.Scatter(
                    x=last_observed.index, 
                    y=last_observed.values[:, feature], 
                    mode='lines',
                    line=dict(color=colors[i % len(colors)], width=2),
                    name=f'Observed {last_observed.columns[feature]}'
                ))
                traces.append(go.Scatter(
                    x=future_df.index, 
                    y=future_df.values[:, feature], 
                    mode='lines',
                    line=dict(color=colors[i % len(colors)], dash='dash', width=2),
                    name=f'Predicted {last_observed.columns[feature]}'
                ))
            fig = go.Figure(data=traces)
            fig.update_layout(
                title=f'Forecast',
                xaxis_title='Time',
                yaxis_title='Feature Value',
                width=1000,
                height=600,
                template='plotly_dark',
                hovermode='x unified'
            )
            fig.show()
        else:
            raise ValueError(f"'{backend}' is not a valid backend. Choose 'matplotlib' or 'plotly'.")
            
    def plot_backtest(self, features, roll_size=5, state='transformed', backend='matplotlib', palette='cool'):
        """
        Plots the results of the backtest for the specified features using either Matplotlib or Plotly.

        Parameters:
        -----------
        features : list[int or str]
            Features to plot (either column indices or names).
        roll_size : int, optional (default=5)
            Number of steps used for the backtest.
        state : str, optional (default='transformed')
            Determines whether to plot data in the 'transformed' or 'recovered' state.
        backend : str, optional (default='matplotlib')
            The plotting backend ('matplotlib' or 'plotly').
        palette : str, optional (default='cool')
            Color palette for the plot.
        """

        valid_backends = ['matplotlib', 'plotly']
        if backend not in valid_backends:
            raise ValueError(f"'{backend}' is not a valid mode. Choose from {valid_backends}.")
        
        valid_states = ['transformed', 'recovered']
        if state not in valid_states:
            raise ValueError(f"'{state}' is not a valid mode. Choose from {valid_states}.")
        observed_df, predicted_df = self.back_test(roll_size=roll_size, state=state)
        
        if isinstance(features, (str, int)):
            features = [features]
        features = [self.recovered_df.columns.tolist().index(feature) if isinstance(feature, str) else feature for feature in features]
 
        if backend == 'matplotlib':
            plt.figure(figsize=(12, 6), facecolor='black')
            cmap = plt.colormaps[palette]
            colors = cmap(np.linspace(0, 1, len(features)))
            
            for idx, feature in enumerate(features):
                # Observado
                plt.plot(
                    observed_df.index, observed_df.values[:, feature],
                    label=f'Observed {observed_df.columns[feature]}',
                    color=colors[idx], linewidth=2
                )
                # Predicho
                plt.plot(
                    predicted_df.index, predicted_df.values[:, feature],
                    linestyle='--', label=f'Predicted {predicted_df.columns[feature]}',
                    color=colors[idx], linewidth=2
                )
            plt.title(f'Backtest', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Time', fontsize=14)
            if state == 'transformed':
                plt.ylabel('Transformed Value', fontsize=14)
            elif state == 'recovered':
                plt.ylabel('$', fontsize=14)
            plt.legend(loc='upper left', fontsize=12, frameon=True, fancybox=True, framealpha=0.7)
            plt.grid(True, which='both', linestyle=':', linewidth=0.5, color='gray')
            plt.tight_layout()
            plt.show()
    
        elif backend == 'plotly':
            traces = []
            colors = px.colors.qualitative.Plotly 
            for i, feature in enumerate(features):
                # Observado
                traces.append(go.Scatter(
                    x=observed_df.index, 
                    y=observed_df.values[:, feature], 
                    mode='lines',
                    line=dict(color=colors[i % len(colors)], width=2),
                    name=f'Observed {observed_df.columns[feature]}'
                ))
                # Predicho
                traces.append(go.Scatter(
                    x=predicted_df.index, 
                    y=predicted_df.values[:, feature], 
                    mode='lines',
                    line=dict(color=colors[i % len(colors)], dash='dash', width=2),
                    name=f'Predicted {predicted_df.columns[feature]}'
                ))
            fig = go.Figure(data=traces)
            fig.update_layout(
                title=f'Backtest',
                xaxis_title='Time',
                yaxis_title='Feature Value',
                width=1000,
                height=600,
                template='plotly_dark',
                hovermode='x unified'
            )
            fig.show()
        else:
            raise ValueError(f"'{backend}' is not a valid backend. Choose 'matplotlib' or 'plotly'.")

    def evaluate (self, roll_size=5, state='transformed'):
        """
        Evaluates the performance of the model using metrics such as MSE, RMSE, MAE, and R².

        Parameters:
        -----------
        roll_size : int, optional (default=5)
            Number of steps used for the backtest.
        state : str, optional (default='transformed')
            Determines whether to evaluate data in the 'transformed' or 'recovered' state.

        Returns:
        --------
        pd.DataFrame
            DataFrame containing the evaluation metrics for each feature.
        """
        valid_states = ['recovered', 'transformed']
        if state not in valid_states:
            raise ValueError(f"'{state}' is not a valid mode. Choose from {valid_states}.")
        observed_df, predicted_df = self.back_test(roll_size=roll_size, state=state)
        evaluation = {}
        mse = []
        rmse = []
        mae = []
        r2 = []
        for feature in observed_df:
            observed_values = observed_df[feature].values
            predicted_values = predicted_df[feature].values
            mse.append(mean_squared_error(observed_values, predicted_values))
            rmse.append(np.sqrt(mse[-1]))
            mae.append(mean_absolute_error(observed_values, predicted_values))
            r2.append(r2_score(observed_values, predicted_values))
        evaluation['MSE'] = mse
        evaluation['RMSE'] = rmse
        evaluation['MAE'] = mae
        evaluation['R2'] = r2
        evaluation = pd.DataFrame(evaluation, index = observed_df.columns)
        evaluation.loc['Mean'] = evaluation.mean()
        return evaluation
    def _generate_dates_ (self, state, df, data_freq):
        """
        Generates a sequence of dates for the forecasted data based on the frequency.

        Parameters:
        -----------
        state : str
            The current state ('transformed' or 'recovered').
        df : pd.DataFrame
            The DataFrame for which to generate dates.
        data_freq : str
            The frequency of the data ('B' for business days).
        """
        bday = pd.offsets.CustomBusinessDay()
        if state == 'recovered':
            dates = self.recovered_df.index
            dates = dates.append(pd.date_range(start=dates[-1] + bday, periods=df.shape[0] - self.recovered_df.shape[0], freq=data_freq))
        elif state == 'transformed':
            dates = self.transformed_df.index
            dates = dates.append(pd.date_range(start=dates[-1] + bday, periods=df.shape[0] - self.transformed_df.shape[0], freq=data_freq))
        return dates
    def _extract_last_window_ (self, X, Ys):
        """
        Extracts the last window of data for forecasting.

        Parameters:
        -----------
        X : np.ndarray
            The input data array (features).
        Ys : np.ndarray
            The target data array (labels).
        """
        feature_windows = {}
        for feature in range (X.shape[2]):
            window = []
            for timestep in range (1, X.shape[1] + Ys.shape[1]):
                if timestep >= X.shape[1]:
                    window.append(Ys[-1, timestep - X.shape[1], feature])
                else:
                    window.append(X[-1, timestep, feature])
            feature_windows[feature] = window
        last_window_array = np.zeros((1, X.shape[1], X.shape[2]))
        for feature in range (X.shape[2]):
            for timestep in range (X.shape[1]):
                last_window_array[-1, timestep, feature] = feature_windows[feature][timestep]
        return last_window_array
    def _forecast_ (self, transformed_df, iterations):
        """
        Performs the core forecast logic, iteratively predicting future values based on the model.

        Parameters:
        -----------
        transformed_df : pd.DataFrame
            The transformed data used for forecasting.
        iterations : int
            Number of future steps to predict.

        Returns:
        --------
        pd.DataFrame
            The full forecasted DataFrame.
        """
        X, Ys = self.post_transformation_pipeline.fit_transform(transformed_df)
        last_window = self._extract_last_window_ (X, Ys)
        new_X = X.copy()
        new_Ys = Ys.copy()
        for i in range (iterations):
            new_X = np.concatenate((new_X, last_window), axis = 0)
            predictions = self.model.predict(last_window)
            new_Ys = np.concatenate((new_Ys, predictions), axis = 0)
            last_window = self._extract_last_window_(new_X, new_Ys)
        full_forecasted_df = self.post_transformation_pipeline.inverse_transform((new_X, new_Ys))
        return full_forecasted_df

class TimeSeriesMonitor ():
    """
    Clase para monitorear y analizar series temporales, con funcionalidades para calcular estadísticas descriptivas, 
    pruebas de estacionaridad, volatilidad, descomposición de series y gráficos interactivos utilizando 
    matplotlib o plotly.

    Atributos:
        df (pd.DataFrame): DataFrame original con las series temporales.
        returns_df (pd.DataFrame): DataFrame con los retornos calculados de las series temporales.
    """
    def __init__ (self, df, returns_df = None, fit_mode='all_positive', transform_mode='returns'):
        """
        Inicializa la clase TimeSeriesMonitor.

        Parámetros:
            df (pd.DataFrame): DataFrame con las series temporales originales.
            returns_df (pd.DataFrame, opcional): DataFrame con los retornos de las series. Si no se proporciona, 
                                                 se calculan automáticamente.
            fit_mode (str, opcional): Modo de ajuste para calcular los retornos, por defecto es 'all_positive'.
        """
        self.df = df
        plt.style.use('dark_background')
        if returns_df is None or not isinstance(returns_df, pd.DataFrame) or returns_df.empty:
            roc_calculator = ROCCalculator(fit_mode=fit_mode, transform_mode=transform_mode)
            returns_df = roc_calculator.fit_transform(df)
        self.returns_df = returns_df
    def describe_statistics (self, returns = False):
        """
        Describe las estadísticas de las series temporales.

        Parámetros:
            returns (bool): Indica si se usan los retornos o los datos originales. Por defecto es False.

        Devuelve:
            pd.DataFrame: Estadísticas descriptivas.
        """
        df = self.returns_df if returns else self.df
        return df.describe()
    def calculate_skewness_kurtosis (self, returns = False):
        """
        Calcula la asimetría (skewness) y la curtosis de las series temporales.

        Parámetros:
            returns (bool): Indica si se usan los retornos o los datos originales. Por defecto es False.

        Devuelve:
            pd.DataFrame: DataFrame con la asimetría y curtosis de las series.
        """
        df = self.returns_df if returns else self.df
        skewness = df.skew()
        kurtosis = df.kurt()
        result = pd.DataFrame({
            'Skewness' : skewness,
            'Kurtosis' : kurtosis
        })
        return result
    def calculate_dispersion_measures (self, returns = False):
        """
        Calcula la varianza y el rango intercuartílico (IQR) de las series temporales.

        Parámetros:
            returns (bool): Indica si se usan los retornos o los datos originales. Por defecto es False.

        Devuelve:
            pd.DataFrame: DataFrame con la varianza y el IQR de las series.
        """
        df = self.returns_df if returns else self.df
        variance = df.var()
        iqr = df.quantile(0.75) - df.quantile(0.25)  # IQR = Q3 - Q1
        result = pd.DataFrame({
            'Variance': variance,
            'IQR': iqr
        })
        return result
    def plot_descriptive_statistics(self, returns=False, backend='matplotlib'):
        """
        Grafica las estadísticas descriptivas de las series temporales.

        Parámetros:
            returns (bool): Indica si se usan los retornos o los datos originales.
            backend (str): Motor de gráficos a usar ('matplotlib' o 'plotly').

        Lanza:
            ValueError: Si el parámetro 'backend' no es 'matplotlib' o 'plotly'.
        """
        df = self.returns_df if returns else self.df
        desc_stats = df.describe().T
        skew_kurtosis = self.calculate_skewness_kurtosis(returns=returns)
        dispersion = self.calculate_dispersion_measures(returns=returns)
    
        titles = ['Mean', 'Variance', 'Skewness', 'Kurtosis']
        data = [
            desc_stats['mean'], 
            dispersion['Variance'], 
            skew_kurtosis['Skewness'], 
            skew_kurtosis['Kurtosis']
        ]
        colors = ['cyan', 'magenta', 'yellow', 'orange']
        y_labels = ['Value', 'Value', 'Skewness', 'Kurtosis']
        if backend == 'matplotlib':
            fig, axs = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle('Descriptive Statistics of Time Series', fontsize=16)
            for i, ax in enumerate(axs.flat):
                ax.bar(df.columns, data[i], color=colors[i], edgecolor='white')
                ax.set_title(titles[i])
                ax.set_ylabel(y_labels[i])
                ax.set_xticks(range(len(df.columns)))
                ax.set_xticklabels(df.columns, rotation=45, ha='right')
                ax.grid(True, color='gray', linestyle='--')
                if titles[i] in ['Skewness', 'Kurtosis']:
                    ax.axhline(0, color='red', linestyle='--', lw=1)
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()
        elif backend == 'plotly':
            fig = make_subplots(rows=2, cols=2, subplot_titles=titles)
            for i, (stat_data, color, y_label, title) in enumerate(zip(data, colors, y_labels, titles)):
                row = i // 2 + 1
                col = i % 2 + 1
                fig.add_trace(go.Bar(
                    x=df.columns,
                    y=stat_data,
                    marker=dict(color=color),
                    name=title
                ), row=row, col=col)
                # Configuración de la línea horizontal en Skewness y Kurtosis
                if title in ['Skewness', 'Kurtosis']:
                    fig.add_hline(y=0, line=dict(color='red', dash='dash'), row=row, col=col)
                # Actualizar ejes
                fig.update_yaxes(title_text=y_label, row=row, col=col)
                fig.update_xaxes(tickangle=45, title_text='Features', row=row, col=col)
            fig.update_layout(
                title='Descriptive Statistics of Time Series',
                width=1000,  # Ancho de la figura
                height=800,  # Alto de la figura
                template='plotly_dark',
                showlegend=False
            )
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def plot_time_series(self, features, returns=False, backend='matplotlib', palette='cool'):
        """
        Grafica las series temporales para las características especificadas.

        Parámetros:
            features (list, str, int o bool): Lista de características a graficar o un solo nombre/índice.
            returns (bool): Indica si se usan los retornos o los datos originales.
            backend (str): Motor de gráficos a usar ('matplotlib' o 'plotly').

        Lanza:
            ValueError: Si el parámetro 'backend' no es 'matplotlib' o 'plotly'.
        """
        df = self.returns_df if returns else self.df
        if isinstance(features, (str, int)):
            features = [features]
        if backend == 'matplotlib':
            plt.figure(figsize=(12, 6), facecolor='black')
            feature_names = []
            cmap = plt.colormaps[palette]
            colors = cmap(np.linspace(0, 1, len(features)))  # Paleta de colores
            for color, feature in zip(colors, features):
                time_series, feature_name = self._read_feature_(df, feature)
                feature_names.append(feature_name)
                mean_value = time_series.mean()
                plt.plot(time_series, label=f'{feature_name}', color=color, linestyle='-')
                plt.axhline(mean_value, color=color, linestyle='--', alpha=0.7, label=f'Media {feature_name}: {mean_value:.4f}')
            plt.title(f'Series Temporales: {", ".join(str(feature) for feature in feature_names)}')
            plt.xlabel('Índice')
            plt.ylabel('Valor')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        elif backend == 'plotly':
            traces = []
            feature_names = []
            colors = px.colors.qualitative.Plotly 
            for i, feature in enumerate(features):
                time_series, feature_name = self._read_feature_(df, feature)
                feature_names.append(feature_name)
                mean_value = time_series.mean()
                # Serie temporal con color diferenciado
                time_series_trace = go.Scatter(
                    x=time_series.index,
                    y=time_series,
                    mode='lines',
                    line=dict(color=colors[i % len(colors)]),
                    name=f'{feature_name}'
                )
                traces.append(time_series_trace)
                # Línea de la media
                mean_line = go.Scatter(
                    x=[time_series.index.min(), time_series.index.max()],
                    y=[mean_value, mean_value],
                    mode='lines',
                    line=dict(color=colors[i % len(colors)], dash='dash'),
                    showlegend=True,
                    name=f'Media {feature_name}: {mean_value:.4f}'
                )
                traces.append(mean_line)
            fig = go.Figure(data=traces)
            fig.update_layout(
                title=f'Series Temporales: {", ".join(str(feature) for feature in feature_names)}',
                xaxis_title='Índice',
                yaxis_title='Valor',
                width=1000,
                height=600,
                template='plotly_dark',
                hovermode='x unified'
            )
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def plot_distribution(self, features, returns=False, backend='matplotlib', bins = 50, palette='cool'):
        """
        Grafica la distribución de las series temporales.

        Parámetros:
            features (list, str o int): Lista de características a analizar, o un solo nombre/índice.
            returns (bool): Indica si se usan los retornos o los datos originales.
            backend (str): Motor de gráficos a usar ('matplotlib' o 'plotly').
            bins (int): Número de bins para el histograma. Por defecto es 50.

        Lanza:
            ValueError: Si el parámetro 'backend' no es 'matplotlib' o 'plotly'.
        """
        if isinstance(features, (str, int)):
            features = [features]
        df = self.returns_df if returns else self.df
        if backend == 'matplotlib':
            plt.figure(figsize=(10, 6))
            cmap = plt.colormaps[palette]
            colors = cmap(np.linspace(0, 1, len(features)))
            feature_names = []
            for color, feature in zip(colors, features):
                time_series, feature_name = self._read_feature_(df, feature)
                feature_names.append(feature_name)
                mean_value = np.mean(time_series)
                # Histograma de la distribución
                plt.hist(time_series, bins=bins, alpha=0.6, color=color, edgecolor='black', density=True, label=f'{feature_name}')
                # Línea de la media
                plt.axvline(mean_value, color=color, linestyle='--', alpha=0.7, label=f'Media {feature_name}: {mean_value:.4f}')
            plt.title(f'Distribuciones: {", ".join(str(feature) for feature in feature_names)}')
            plt.xlabel('Valor')
            plt.ylabel('Densidad')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        elif backend == 'plotly':
            traces = []
            colors = px.colors.qualitative.Plotly  # Paleta de colores cualitativos
            feature_names = []
            for i, feature in enumerate(features):
                time_series, feature_name = self._read_feature_(df, feature)
                feature_names.append(feature_name)
                mean_value = np.mean(time_series)
                # Histograma de la distribución
                hist_data = go.Histogram(
                    x=time_series,
                    nbinsx=bins,
                    histnorm='probability density',
                    marker=dict(color=colors[i % len(colors)], line=dict(color='black', width=1)),
                    opacity=0.6,
                    name=f'{feature_name}'
                )
                traces.append(hist_data)
                # Línea de la media
                mean_line = go.Scatter(
                    x=[mean_value, mean_value],
                    y=[0, max(np.histogram(time_series, bins=30, density=True)[0])],
                    mode='lines',
                    line=dict(color=colors[i % len(colors)], dash='dash'),
                    showlegend=True,
                    name=f'Media {feature_name}: {mean_value:.4f}'
                )
                traces.append(mean_line)
            fig = go.Figure(data=traces)
            fig.update_layout(
                title=f'Distribuciones: {", ".join(str(feature) for feature in feature_names)}',
                xaxis_title='Valor',
                yaxis_title='Densidad',
                width=1000,
                height=600,
                template='plotly_dark',
                hovermode='x unified'
            )
            fig.update_yaxes(range=[0, max([np.histogram(self._read_feature_(df, f)[0], bins=30, density=True)[0].max() for f in features]) * 1.1])
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def get_feature_autoc (self, feature, lags = 40, returns = False):
        """
        Calcula la función de autocorrelación (ACF) y autocorrelación parcial (PACF) para una característica.

        Parámetros:
            feature (str o int): Nombre o índice de la característica a analizar.
            lags (int): Número de lags a calcular. Por defecto es 40.
            returns (bool): Indica si se usan los retornos o los datos originales.

        Devuelve:
            pd.DataFrame: DataFrame con los valores de ACF y PACF.
        """
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        acf_values = acf(time_series, nlags = lags)
        pacf_values = pacf(time_series, nlags = lags)
        df = pd.DataFrame([acf_values, pacf_values]).T
        df.columns = ['ACF', 'PACF']
        df.index = [f'lag {i}' for i in range (lags + 1)]
        return df
    def get_significant_lags (self, top=5, func='ACF', scorer = 'mean', lags = 40, returns = False, absolute = False):
        """
        Identifica los lags más significativos según la función especificada.

        Parámetros:
            top (int): Número de lags más significativos a retornar.
            func (str): Tipo de función ('ACF' o 'PACF').
            scorer (str): Método de agregación ('mean' o 'sum').
            lags (int): Número de lags a considerar.
            returns (bool): Indica si se usan los retornos o los datos originales.

        Devuelve:
            pd.DataFrame: DataFrame con los lags más significativos.
        
        Lanza:
            ValueError: Si el parámetro func o scorer no es válido.
        """
        df = self.returns_df if returns else self.df
        valid_scorers = ['mean', 'sum']
        valid_funcs = ['ACF', 'PACF']
        if func not in valid_funcs:
            raise ValueError(f"'{func}' is not a valid mode. Choose from {valid_funcs}.")
        if scorer not in valid_scorers:
            raise ValueError(f"'{scorer}' is not a valid mode. Choose from {valid_scorers}.")
        func_dict = {}
        for feature in range (df.shape[1]):
            current_func_results = self.get_feature_autoc(feature=feature, lags=lags, returns = returns)[func].values
            func_dict[feature] = current_func_results
        func_df = pd.DataFrame(func_dict, index=[f'lag {i}' for i in range (lags + 1)])
        if scorer == 'mean':
            func_df[scorer] = func_df.mean(axis = 1)
        elif scorer == 'sum':
            func_df[scorer] = func_df.sum(axis = 1)
        if absolute:
            func_df = func_df.abs()
        top_rows = func_df.nlargest(top + 1, scorer)#.drop(columns=scorer)
        return top_rows
    def plot_acf_pacf(self, features, lags=40, returns=False, backend='matplotlib', palette='cool'):
        """
        Grafica la función de autocorrelación (ACF) y autocorrelación parcial (PACF) para múltiples características.

        Parámetros:
            features (list, str o int): Características a analizar.
            lags (int): Número de lags para calcular ACF y PACF.
            returns (bool): Indica si se usan los retornos o los datos originales.
            backend (str): Motor de gráficos a usar ('matplotlib' o 'plotly').

        Lanza:
            ValueError: Si el parámetro backend no es 'matplotlib' o 'plotly'.
        """
        if isinstance(features, (str, int)):
            features = [features]
        df = self.returns_df if returns else self.df
        if backend == 'matplotlib':
            cmap = plt.colormaps[palette]
            colors = cmap(np.linspace(0, 1, len(features)))
            fig, ax = plt.subplots(2, 1, figsize=(12, 8), facecolor='black')
            for color, feature in zip(colors, features):
                time_series, feature_name = self._read_feature_(df, feature)
                # ACF (excluyendo lag 0)
                acf_values = acf(time_series, nlags=lags)[1:]  # Excluir lag 0
                pacf_values = pacf(time_series, nlags=lags)[1:]  # Excluir lag 0
                lags_without_0 = np.arange(1, len(acf_values) + 1)  # Lags a partir de 1
                
                # ACF
                ax[0].stem(lags_without_0, acf_values, linefmt='-', markerfmt='o', basefmt=" ", label=f'ACF for {feature_name}')
                ax[0].set_title('Autocorrelation Function (ACF)', color='white')
                ax[0].set_facecolor('black')
                ax[0].grid(True, color='gray', linestyle='--')
                ax[0].tick_params(axis='x', colors='white')
                ax[0].tick_params(axis='y', colors='white')
                ax[0].legend()
        
                # PACF
                ax[1].stem(lags_without_0, pacf_values, linefmt='-', markerfmt='o', basefmt=" ", label=f'PACF for {feature_name}')
                ax[1].set_title('Partial Autocorrelation Function (PACF)', color='white')
                ax[1].set_facecolor('black')
                ax[1].grid(True, color='gray', linestyle='--')
                ax[1].tick_params(axis='x', colors='white')
                ax[1].tick_params(axis='y', colors='white')
                ax[1].legend()
            
            plt.tight_layout()
            plt.show()


        elif backend == 'plotly':
            traces = []
            colors = px.colors.qualitative.Plotly  # Paleta de colores cualitativos
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(
                'Autocorrelation Function (ACF)', 
                'Partial Autocorrelation Function (PACF)'
            ))
            for i, feature in enumerate(features):
                time_series, feature_name = self._read_feature_(df, feature)
                # Calcular los valores de ACF y PACF excluyendo lag 0
                acf_values = acf(time_series, nlags=lags)[1:]  # Excluir lag 0
                pacf_values = pacf(time_series, nlags=lags)[1:]  # Excluir lag 0
                lags_without_0 = list(range(1, len(acf_values) + 1))  # Lags a partir de 1
                
                # ACF
                fig.add_trace(go.Bar(
                    x=lags_without_0,
                    y=acf_values,
                    name=f'ACF for {feature_name}',
                    marker=dict(color=colors[i % len(colors)])
                ), row=1, col=1)
                
                # PACF
                fig.add_trace(go.Bar(
                    x=lags_without_0,
                    y=pacf_values,
                    name=f'PACF for {feature_name}',
                    marker=dict(color=colors[i % len(colors)])
                ), row=2, col=1)
            
            fig.update_layout(
                height=800,  # Alto de la figura
                width=1200,  # Ancho de la figura
                template='plotly_dark',
                showlegend=True,
                title_text='ACF and PACF for Multiple Features',
                hovermode='x unified'
            )
            fig.update_xaxes(title_text='Lags', row=2, col=1)
            fig.update_yaxes(title_text='Correlation', row=1, col=1)
            fig.update_yaxes(title_text='Partial Correlation', row=2, col=1)
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def lag_scatter(self, features, lag=1, returns=False, backend='matplotlib', palette='cool'):
        """
        Grafica la correlación de series desplazadas en el tiempo.

        Parámetros:
            features (list, str o int): Características a analizar.
            lag (int): Desplazamiento de la serie en el tiempo.
            returns (bool): Indica si se usan los retornos o los datos originales.
            backend (str): Motor de gráficos a usar ('matplotlib' o 'plotly').

        Lanza:
            ValueError: Si el parámetro backend no es 'matplotlib' o 'plotly'.
        """
        if isinstance(features, (str, int)):
            features = [features]
        df = self.returns_df if returns else self.df
        if backend == 'matplotlib':
            cmap = plt.colormaps[palette]
            colors = cmap(np.linspace(0, 1, len(features)))  # Paleta de colores
            plt.figure(figsize=(10, 6))
            for color, feature in zip(colors, features):
                time_series, feature_name = self._read_feature_(df, feature)
                t_series = time_series[lag:]
                t_lag_series = time_series[:-lag]
                # Graficar la serie desplazada
                plt.plot(t_series, t_lag_series, 'o', label=f'{feature_name}', color=color, alpha=0.6)
            # Configuración del gráfico
            plt.xlabel('t series')
            plt.ylabel('t-lag series')
            plt.title(f'Lagged Correlation for Multiple Features')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        elif backend == 'plotly':
            traces = []
            colors = px.colors.qualitative.Plotly  # Paleta de colores cualitativos
            fig = go.Figure()
            for i, feature in enumerate(features):
                time_series, feature_name = self._read_feature_(df, feature)
                t_series = time_series[lag:]
                t_lag_series = time_series[:-lag]
                # Agregar el scatter plot para cada característica
                fig.add_trace(go.Scatter(
                    x=t_series, 
                    y=t_lag_series, 
                    mode='markers', 
                    marker=dict(color=colors[i % len(colors)]),
                    name=f'Lag Scatter for {feature_name}'
                ))
            # Configuración de la figura
            fig.update_layout(
                title='Lagged Correlation for Multiple Features',
                xaxis_title='t series',
                yaxis_title='t-lag series',
                width=1000,  # Ancho de la figura
                height=600,  # Alto de la figura
                template='plotly_dark',
                hovermode='closest'  # Muestra información más cercana al cursor
            )
            
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def decompose_series (self, feature, model='additive', freq=None, returns = False):
        """
        Descompone una serie temporal en componentes (tendencia, estacionalidad, residuales).

        Parámetros:
            feature (str o int): Característica a descomponer.
            model (str): Tipo de modelo ('additive' o 'multiplicative').
            freq (int): Frecuencia de la estacionalidad.
            returns (bool): Indica si se usan los retornos o los datos originales.

        Devuelve:
            tuple: Componentes de tendencia, estacionalidad y residuales.
        """
        df = self.returns_df if returns else self.df
        time_series, _ = self._read_feature_(df, feature)
        decomposition = seasonal_decompose(time_series, model=model, period=freq)
        trend, seasonality, residuals = decomposition.trend, decomposition.seasonal, decomposition.resid
        return trend, seasonality, residuals
    def plot_decomposed_series(self, features, model='additive', freq=None, returns=False, backend='matplotlib', palette='cool'):
        """
        Grafica la serie original y sus componentes descompuestos (tendencia, estacionalidad, residuales).

        Parámetros:
            features (list, str o int): Características a analizar.
            model (str): Tipo de modelo para la descomposición.
            freq (int): Frecuencia de la estacionalidad.
            returns (bool): Indica si se usan los retornos o los datos originales.
            backend (str): Motor de gráficos a usar ('matplotlib' o 'plotly').

        Lanza:
            ValueError: Si el parámetro backend no es 'matplotlib' o 'plotly'.
        """
        if isinstance(features, (str, int)):
            features = [features]
        df = self.returns_df if returns else self.df
        # Colores para el caso de una sola característica
        single_feature_colors = ['cyan', 'magenta', 'yellow', 'orange']
        if backend == 'matplotlib':
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10), facecolor='black')
            if len(features) == 1:
                colors = single_feature_colors
            else:
                cmap = plt.colormaps[palette]
                colors = cmap(np.linspace(0, 1, len(features)))
            for color, feature in zip(colors, features):
                time_series, feature_name = self._read_feature_(df, feature)
                trend, seasonality, residuals = self.decompose_series(feature, model, freq, returns=returns)
                # Graficar la serie original
                ax1.plot(time_series, label=f'Original ({feature_name})', color=color if len(features) > 1 else single_feature_colors[0])
                ax1.set_title('Original Series', color='white')
                ax1.set_facecolor('black')
                ax1.grid(True, color='gray', linestyle='--')
                ax1.tick_params(axis='x', colors='white')
                ax1.tick_params(axis='y', colors='white')
                # Graficar la tendencia
                ax2.plot(trend, label=f'Trend ({feature_name})', color=color if len(features) > 1 else single_feature_colors[1])
                ax2.set_title('Trend', color='white')
                ax2.set_facecolor('black')
                ax2.grid(True, color='gray', linestyle='--')
                ax2.tick_params(axis='x', colors='white')
                ax2.tick_params(axis='y', colors='white')
                # Graficar la estacionalidad
                ax3.plot(seasonality, label=f'Seasonality ({feature_name})', color=color if len(features) > 1 else single_feature_colors[2])
                ax3.set_title('Seasonality', color='white')
                ax3.set_facecolor('black')
                ax3.grid(True, color='gray', linestyle='--')
                ax3.tick_params(axis='x', colors='white')
                ax3.tick_params(axis='y', colors='white')
                # Graficar los residuales
                ax4.plot(residuals, label=f'Residuals ({feature_name})', color=color if len(features) > 1 else single_feature_colors[3])
                ax4.set_title('Residuals', color='white')
                ax4.set_facecolor('black')
                ax4.grid(True, color='gray', linestyle='--')
                ax4.tick_params(axis='x', colors='white')
                ax4.tick_params(axis='y', colors='white')
            ax1.legend(loc='upper right')
            ax2.legend(loc='upper right')
            ax3.legend(loc='upper right')
            ax4.legend(loc='upper right')
            plt.tight_layout()
            plt.show()
        elif backend == 'plotly':
            fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(
                'Original Series', 'Trend', 'Seasonality', 'Residuals'))
            colors = px.colors.qualitative.Plotly if len(features) > 1 else single_feature_colors
            for i, feature in enumerate(features):
                time_series, feature_name = self._read_feature_(df, feature)
                trend, seasonality, residuals = self.decompose_series(feature, model, freq, returns=returns)
                # Serie original
                fig.add_trace(go.Scatter(x=time_series.index, y=time_series, mode='lines', name=f'Original ({feature_name})',
                                         line=dict(color=colors[0 if len(features) == 1 else i % len(colors)])), row=1, col=1)
                # Tendencia
                fig.add_trace(go.Scatter(x=trend.index, y=trend, mode='lines', name=f'Trend ({feature_name})',
                                         line=dict(color=colors[1 if len(features) == 1 else i % len(colors)])), row=2, col=1)
                # Estacionalidad
                fig.add_trace(go.Scatter(x=seasonality.index, y=seasonality, mode='lines', name=f'Seasonality ({feature_name})',
                                         line=dict(color=colors[2 if len(features) == 1 else i % len(colors)])), row=3, col=1)
                # Residuales
                fig.add_trace(go.Scatter(x=residuals.index, y=residuals, mode='lines', name=f'Residuals ({feature_name})',
                                         line=dict(color=colors[3 if len(features) == 1 else i % len(colors)])), row=4, col=1)
            fig.update_layout(
                height=1000,  # Alto de la figura
                width=1200,   # Ancho de la figura
                template='plotly_dark',
                showlegend=True,
                hovermode='x unified',
                title_text='Decomposition for Multiple Features' if len(features) > 1 else f'Decomposition of {features[0]}'
            )
            fig.update_layout(
                legend=dict(
                    x=0.5,  # Coloca la leyenda en la mitad del gráfico horizontalmente
                    y=1.05,  # Coloca la leyenda arriba del gráfico
                    xanchor='center',  # Centra la leyenda horizontalmente
                    orientation='h',  # Leyenda horizontal
                    bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
                )
            )
            fig.update_xaxes(title_text='Time', row=4, col=1)
            fig.update_yaxes(title_text='Values')
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def stationarity_test(self, feature, returns = False):
        """
        Realiza pruebas de estacionaridad (ADF y KPSS) para una característica.

        Parámetros:
            feature (str o int): Característica a analizar.
            returns (bool): Indica si se usan los retornos o los datos originales.

        Devuelve:
            pd.DataFrame: Resultados de las pruebas de estacionaridad.
        """
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        adf_result = self._adfuller_(time_series)
        kpss_result = self._kpss_(time_series)
        test_results = {
            'ADF Test': adf_result,
            'KPSS Test': kpss_result
        }
        result = self._clean_stat_result_(test_results)
        return result
    def stationarity_test_conclusion(self, feature, returns = False):
        """
        Imprime conclusiones de las pruebas de estacionaridad.

        Parámetros:
            feature (str o int): Característica a analizar.
            returns (bool): Indica si se usan los retornos o los datos originales.
        """
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        results = self.stationarity_test(feature, returns = returns)
        for row_idx in range (results.shape[0]):
            test_name = results.index[row_idx]
            statistic = results.iat[row_idx, 0]
            if test_name == 'ADF Test':
                print (test_name)
                if statistic < results.iat[row_idx, 2]:
                    print("Estacionaria con un 99% de confianza")
                elif statistic < results.iat[row_idx, 3]:
                    print("Estacionaria con un 95% de confianza")
                elif statistic < results.iat[row_idx, 4]:
                    print("Estacionaria con un 90% de confianza")
                else:
                    print("No es estacionaria")
            elif test_name == 'KPSS Test':
                print (test_name)
                if statistic > results.iat[row_idx, 2]:
                    print("No estacionaria con un 99% de confianza")
                elif statistic > results.iat[row_idx, 3]:
                    print("No estacionaria con un 95% de confianza")
                elif statistic > results.iat[row_idx, 4]:
                    print("No estacionaria con un 90% de confianza")
                else:
                    print("Es estacionaria")
    def rolling_volatility(self, features, window=20, returns=True, plot_original=False, peaks=False, threshold_factor=2, backend='matplotlib', palette='cool'):
        """
        Calcula y grafica la volatilidad en ventanas móviles para múltiples características.

        Parámetros:
            features (list, str o int): Características a analizar.
            window (int): Tamaño de la ventana móvil.
            returns (bool): Indica si se usan los retornos o los datos originales.
            plot_original (bool): Indica si se grafican las series originales.
            peaks (bool): Indica si se destacan picos en la volatilidad.
            threshold_factor (float): Factor para definir umbral de picos.
            backend (str): Motor de gráficos a usar ('matplotlib' o 'plotly').

        Lanza:
            ValueError: Si el parámetro backend no es 'matplotlib' o 'plotly'.
        """
        if isinstance(features, (str, int)):
            features = [features]
        df = self.returns_df if returns else self.df
        if backend == 'matplotlib':
            cmap = plt.colormaps[palette]
            colors = cmap(np.linspace(0, 1, len(features)))  # Paleta de colores
            plt.figure(figsize=(12, 6), facecolor='black')
            for color, feature in zip(colors, features):
                time_series, feature_name = self._read_feature_(df, feature)
                rolling_volatility = time_series.rolling(window=window).std()
                if plot_original:
                    plt.plot(time_series, color=color, alpha=0.6, label=f'Serie Original ({feature_name})')
                plt.plot(rolling_volatility, color=color, label=f'Volatilidad ({feature_name}, {window}-ventana)')
                if peaks:
                    threshold = rolling_volatility.mean() + threshold_factor * rolling_volatility.std()
                    peaks_values = rolling_volatility[rolling_volatility > threshold]
                    plt.scatter(peaks_values.index, peaks_values, color='red', marker='o', label=f'Picos de Volatilidad ({feature_name})')
                    plt.axhline(threshold, color='yellow', linestyle='--', label=f'Umbral ({threshold_factor}x Desv. Est., {feature_name})')
            # Configuración del gráfico
            plt.title('Volatilidad en Ventanas Móviles para Múltiples Características', color='white')
            plt.xlabel('Tiempo', color='white')
            plt.ylabel('Volatilidad', color='white')
            plt.grid(True, color='gray', linestyle='--')
            plt.tick_params(axis='x', colors='white')
            plt.tick_params(axis='y', colors='white')
            plt.gca().set_facecolor('black')
            plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize='small')
            plt.tight_layout()
            plt.show()
        elif backend == 'plotly':
            fig = go.Figure()
            colors = px.colors.qualitative.Plotly
            for i, feature in enumerate(features):
                time_series, feature_name = self._read_feature_(df, feature)
                rolling_volatility = time_series.rolling(window=window).std()
                if plot_original:
                    fig.add_trace(go.Scatter(
                        x=time_series.index, 
                        y=time_series, 
                        mode='lines', 
                        name=f'Serie Original ({feature_name})', 
                        line=dict(color=colors[i % len(colors)]), 
                        opacity=0.6 
                    ))
                fig.add_trace(go.Scatter(
                    x=rolling_volatility.index, 
                    y=rolling_volatility, 
                    mode='lines', 
                    name=f'Volatilidad ({feature_name}, {window}-ventana)', 
                    line=dict(color=colors[i % len(colors)])
                ))
                if peaks:
                    threshold = rolling_volatility.mean() + threshold_factor * rolling_volatility.std()
                    peaks_values = rolling_volatility[rolling_volatility > threshold]
                    fig.add_trace(go.Scatter(
                        x=peaks_values.index, 
                        y=peaks_values, 
                        mode='markers', 
                        name=f'Picos de Volatilidad ({feature_name})', 
                        marker=dict(color='red', symbol='circle')
                    ))
                    fig.add_hline(
                        y=threshold, 
                        line=dict(color='yellow', dash='dash'), 
                        annotation_text=f'Umbral ({threshold_factor}x Desv. Est., {feature_name})', 
                        annotation_position='top right'
                    )
            fig.update_layout(
                title='Volatilidad en Ventanas Móviles para Múltiples Características',
                xaxis_title='Tiempo',
                yaxis_title='Volatilidad',
                template='plotly_dark',
                width=1200,
                height=600,  
                hovermode='x unified',
                legend=dict(
                    x=0.5,
                    y=-0.2,
                    xanchor='center',
                    orientation='h',
                    bgcolor='rgba(0, 0, 0, 0)'
                )
            )
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def _adfuller_(self, time_series):
        """
        Realiza la prueba ADF para una serie temporal.

        Parámetros:
            time_series (pd.Series): Serie temporal a analizar.

        Devuelve:
            dict: Resultados de la prueba ADF.
        """
        adf_result = adfuller(time_series, autolag='AIC')
        adf_output = {
            'ADF Statistic': adf_result[0],
            'p-value': adf_result[1],
            'Critical Values': adf_result[4]
        }
        return adf_output
    def _kpss_ (self, time_series):
        """
        Realiza la prueba KPSS para una serie temporal.

        Parámetros:
            time_series (pd.Series): Serie temporal a analizar.

        Devuelve:
            dict: Resultados de la prueba KPSS.
        """
        kpss_result = kpss(time_series, regression='c')
        kpss_output = {
            'KPSS Statistic': kpss_result[0],
            'p-value': kpss_result[1],
            'Critical Values': kpss_result[3]
        }
        return kpss_output

    def _read_feature_ (self, df, feature):
        """
        Lee una característica de un DataFrame.

        Parámetros:
            df (pd.DataFrame): DataFrame que contiene la característica.
            feature (str o int): Nombre o índice de la característica.

        Devuelve:
            tuple: Serie temporal y nombre de la característica.
        """
        if type(feature) == str:
            feature_idx = self.df.columns.tolist().index(feature)
            time_series = df.iloc[:, feature_idx]
            feature_name = feature
        elif type(feature) == int:
            time_series = df.iloc[:, feature]
            feature_name = self.df.columns[feature]
        return time_series, feature_name
    def _clean_stat_result_ (self, test_results):
        """
        Limpia y organiza los resultados de las pruebas estadísticas.

        Parámetros:
            test_results (dict): Resultados de las pruebas estadísticas.

        Devuelve:
            pd.DataFrame: DataFrame con los resultados organizados.
        """
        data = {
            'Test': ['ADF Test', 'KPSS Test'],
            'Statistic': [test_results['ADF Test']['ADF Statistic'], test_results['KPSS Test']['KPSS Statistic']],
            'p-value': [test_results['ADF Test']['p-value'], test_results['KPSS Test']['p-value']],
            'Critical Value 1%': [test_results['ADF Test']['Critical Values']['1%'], test_results['KPSS Test']['Critical Values']['1%']],
            'Critical Value 5%': [test_results['ADF Test']['Critical Values']['5%'], test_results['KPSS Test']['Critical Values']['5%']],
            'Critical Value 10%': [test_results['ADF Test']['Critical Values']['10%'], test_results['KPSS Test']['Critical Values']['10%']]
        }
        df = pd.DataFrame(data)
        df.set_index('Test', inplace = True)
        return df
    def calculate_var(self, feature, confidence_level=0.95, method='parametric', returns = True):
        """
        Calcula el Value at Risk (VaR) para la serie temporal especificada.

        Parámetros:
            feature (str o int): Característica a analizar.
            confidence_level (float): Nivel de confianza para el VaR. Por defecto es 0.95.
            method (str): Método para calcular el VaR ('parametric' o 'historical').
            returns (bool): Indica si se usan los retornos o los datos originales.

        Devuelve:
            float: Valor calculado del VaR.

        Lanza:
            ValueError: Si el método no es 'parametric' o 'historical'.
        """
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        if method == 'parametric':
            # VaR Paramétrico: Supone distribución normal de los retornos
            mean_return = time_series.mean()
            std_dev = time_series.std()
            z_score = np.abs(np.percentile(time_series, (1 - confidence_level) * 100))
            var = z_score * std_dev - mean_return
        elif method == 'historical':
            # VaR Histórico: Basado en el percentil de los retornos históricos
            var = np.percentile(time_series, (1 - confidence_level) * 100)
        else:
            raise ValueError("El método debe ser 'parametric' o 'historical'.")
        return var