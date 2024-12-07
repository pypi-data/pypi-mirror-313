import numpy as np

class Fit():
    """
    Class for wrapping all relevant information for a fitted function
    Fit(model, params, cov, x: np.ndarray, y: np.ndarray, upper: np.ndarray, lower: np.ndarray, dx: np.ndarray = None, dy: np.ndarray = None, resampled_points: np.ndarray = None)
    """

    def __init__(self, model, params, cov, x: np.ndarray, upper: np.ndarray, lower: np.ndarray, resampled_points: np.ndarray = None):
        self.model = model
        self.x = x

        self.upper = upper
        self.lower = lower 

        self.params = params
        self.cov = cov

        if resampled_points is None:
            self.resampled_points = x
        else:
            self.resampled_points = resampled_points
