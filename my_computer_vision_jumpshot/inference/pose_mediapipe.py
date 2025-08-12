from dataclasses import dataclass
from typing import List, Optional, Tuple
import numpy as np
import mediapipe as mp
import cv2

@dataclass
class PoseResult:
    # 33 keypoints: (x, y, z, visibility) in image pixel coords
    keypoints: Optional[np.ndarray]  # shape [33,4] or None when not detected

class MediaPipePose:
    def __init__(self, model_complexity: int = 1, min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        self._pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=model_complexity,
            enable_segmentation=False,
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def __call__(self, frame_bgr) -> PoseResult:
        # MediaPipe expects RGB
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._pose.process(rgb)

        if not result.pose_landmarks:
            return PoseResult(keypoints=None)

        kps = []
        for lm in result.pose_landmarks.landmark:
            x = lm.x * w
            y = lm.y * h
            z = lm.z  # normalized depth-ish, leave unitless
            v = lm.visibility
            kps.append((x, y, z, v))
        return PoseResult(keypoints=np.array(kps, dtype=np.float32))

    def close(self):
        self._pose.close()
