import cv2
import numpy as np

# A simple skeleton connectivity (subset; MediaPipe has 33 points).
# You can refine this list later (e.g., full landmark graph).
POSE_EDGES = [
    (11,13), (13,15),  # left arm
    (12,14), (14,16),  # right arm
    (11,12),           # shoulders
    (23,25), (25,27),  # left leg
    (24,26), (26,28),  # right leg
    (23,24),           # hips
]

def draw_pose(frame_bgr, keypoints, score_thresh: float = 0.5):
    if keypoints is None:
        return frame_bgr
    out = frame_bgr.copy()

    # draw points
    for i, (x, y, z, v) in enumerate(keypoints):
        if v < score_thresh: 
            continue
        cv2.circle(out, (int(x), int(y)), 3, (0, 255, 255), -1)

    # draw edges
    for i, j in POSE_EDGES:
        xi, yi, zi, vi = keypoints[i]
        xj, yj, zj, vj = keypoints[j]
        if vi >= score_thresh and vj >= score_thresh:
            cv2.line(out, (int(xi), int(yi)), (int(xj), int(yj)), (0, 255, 0), 2)

    return out
