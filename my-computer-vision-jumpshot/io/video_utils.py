from dataclasses import dataclass
from typing import Iterator, Optional, Tuple
import cv2

@dataclass
class VideoReader:
    path: str

    def __iter__(self) -> Iterator[Tuple[int, float, "cv2.Mat"]]:
        cap = cv2.VideoCapture(self.path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {self.path}")
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        i = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            yield i, i / fps, frame
            i += 1
        cap.release()

class VideoWriter:
    def __init__(self, path: str, fps: float, frame_size: Tuple[int, int]):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self._writer = cv2.VideoWriter(path, fourcc, fps, frame_size)

    def write(self, frame):
        self._writer.write(frame)

    def close(self):
        self._writer.release()
