from typing import List, Tuple
import numpy as np
from norfair import Detection, Tracker

def euclidean_distance(detection: Detection, tracked_object) -> float:
    return np.linalg.norm(detection.points - tracked_object.estimate)

class SimpleTracker:
    """Wrap Norfair for single-class tracking (e.g., basketball)."""
    def __init__(self, distance_threshold: float = 30):
        self.tracker = Tracker(distance_function=euclidean_distance,
                               distance_threshold=distance_threshold)

    def update(self, centers: List[Tuple[float, float]]):
        dets = [Detection(np.array([[x, y]])) for (x, y) in centers]
        return self.tracker.update(detections=dets)
