import argparse
import os
import cv2
from .io.video_utils import VideoReader, VideoWriter
from .inference.pose_mediapipe import MediaPipePose
from .io.renderer import draw_pose
from .processing.smoothing import EMA

def main():
    parser = argparse.ArgumentParser("my-computer-vision-jumpshot")
    parser.add_argument("--video", required=True, help="Path to input video")
    parser.add_argument("--out", default="examples/sample_output/shot_00.mp4", help="Output video path")
    parser.add_argument("--fps", type=float, default=None, help="Override FPS (optional)")
    args = parser.parse_args()

    reader = VideoReader(args.video)
    pose = MediaPipePose(model_complexity=1)
    smoother = EMA(alpha=0.25)

    writer = None
    try:
        for i, t, frame in reader:
            if writer is None:
                h, w = frame.shape[:2]
                # Derive FPS from file if not forced
                cap = cv2.VideoCapture(args.video)
                fps = args.fps or cap.get(cv2.CAP_PROP_FPS) or 30.0
                cap.release()
                os.makedirs(os.path.dirname(args.out), exist_ok=True)
                writer = VideoWriter(args.out, fps=fps, frame_size=(w, h))

            res = pose(frame)
            kps = smoother(res.keypoints) if res.keypoints is not None else None
            vis = draw_pose(frame, kps)
            writer.write(vis)

        print(f"✅ Wrote: {args.out}")
    finally:
        if writer:
            writer.close()
        pose.close()

if __name__ == "__main__":
    main()
