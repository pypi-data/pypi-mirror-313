import numpy as np

class MonteCarloSimulator:
    """
    A class for simulating scenarios using the Monte Carlo method on a dataset. This simulator
    generates paths based on the mean and standard deviation of an input array and optionally 
    updates the statistics of each feature after every simulation step.

    Attributes
    ----------
    steps : int
        Number of simulation steps (time steps) to generate.
    paths : int
        Number of Monte Carlo simulation paths (scenarios) to generate.

    Methods
    -------
    simulate(X, axis=0, update=False):
        Runs the Monte Carlo simulation on the input data array `X`.
    """

    def __init__(self, steps, paths):
        """
        Initializes the MonteCarloSimulator with the specified number of steps and paths.

        Parameters
        ----------
        steps : int
            The number of time steps in each simulation.
        paths : int
            The number of simulation paths to generate.
        """
        self.steps = steps
        self.paths = paths

    def simulate(self, X, axis=0, update=False):
        """
        Performs Monte Carlo simulations based on the statistics (mean and standard deviation) of the input array `X`.
        
        If `update` is True, the mean and standard deviation are recalculated for each feature at every simulation step.
        
        Parameters
        ----------
        X : np.ndarray
            The input data array used to initialize the simulation's statistics. Must be a 2D array.
        axis : int, optional
            The axis along which to calculate the statistics. Default is 0 (rows).
        update : bool, optional
            If True, updates the mean and standard deviation after each simulation step. Default is False.
        
        Returns
        -------
        simulations : np.ndarray
            A 3D array of shape (steps, paths, features) representing the simulated paths.
        
        Raises
        ------
        ValueError
            If `X` is not a 2D numpy array, contains NaNs, or if `axis` is not 0 or 1.
        """

        axles = [0, 1]
        if not isinstance(X, np.ndarray):
            raise ValueError("X must be an array")
        if X.ndim != 2:
            raise ValueError("Array must be bidimensional")
        if np.isnan(X).any():
            raise ValueError("Array contains NaNs")
        if axis not in axles:
            raise ValueError("Axis out of range")
        axles.remove(axis)
        if update not in [True, False]:
            raise ValueError("update not a boolean parameter")

        if update:
            std = np.zeros((1, self.paths, X.shape[axles[0]]))
            mean = np.zeros((1, self.paths, X.shape[axles[0]]))
            for feature in range(X.shape[axles[0]]):
                std[0, :, feature] = np.repeat(np.std(np.take(X, feature, axis=axles[0])), self.paths)
                mean[0, :, feature] = np.repeat(np.mean(np.take(X, feature, axis=axles[0])), self.paths)
            
            simulations = np.zeros((self.steps, self.paths, X.shape[axles[0]]))
            for step in range(self.steps):
                current_simulations = np.random.normal(loc=mean, scale=std, size=(1, self.paths, X.shape[axles[0]]))
                for feature in range(X.shape[axles[0]]):
                    std[0, :, feature] = np.std(
                        np.concatenate([np.tile(np.take(X, feature, axis=axles[0]).reshape(-1, 1), self.paths),
                                        np.take(current_simulations[0, :, :], feature, axis=1).reshape(1, -1)], axis=0),
                        axis=0
                    )
                    mean[0, :, feature] = np.mean(
                        np.concatenate([np.tile(np.take(X, feature, axis=axles[0]).reshape(-1, 1), self.paths),
                                        np.take(current_simulations[0, :, :], feature, axis=1).reshape(1, -1)], axis=0),
                        axis=0
                    )
                simulations[step, :, :] = current_simulations[0, :, :]

        else:
            std = np.std(X, axis=axis)
            mean = np.mean(X, axis=axis)
            simulations = np.random.normal(loc=mean, scale=std, size=(self.steps, self.paths, X.shape[axles[0]]))

        return simulations
