import numpy as np

class EMA:
    """Simple exponential moving average for keypoints (per-dimension)."""
    def __init__(self, alpha: float = 0.2):
        self.alpha = alpha
        self.state = None

    def __call__(self, arr: np.ndarray) -> np.ndarray:
        if arr is None:
            return None
        if self.state is None:
            self.state = arr.copy()
        else:
            self.state = self.alpha * arr + (1 - self.alpha) * self.state
        return self.state
