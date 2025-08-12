from dataclasses import dataclass
from typing import List, Dict
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2

@dataclass
class Detection:
    boxes: torch.Tensor   # [N,4] xyxy
    scores: torch.Tensor  # [N]
    labels: torch.Tensor  # [N] int

class TorchVisionDetector:
    def __init__(self, device: str = "cpu", score_thresh: float = 0.5):
        self.model = fasterrcnn_resnet50_fpn_v2(weights="DEFAULT").eval().to(device)
        self.device = device
        self.score_thresh = score_thresh

    @torch.no_grad()
    def __call__(self, frame_bgr) -> Detection:
        # model expects float tensors [C,H,W] in 0..1 RGB
        import cv2, torchvision.transforms.functional as F
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        t = torch.from_numpy(rgb).permute(2,0,1).float() / 255.0
        t = t.to(self.device)
        out: List[Dict[str, torch.Tensor]] = self.model([t])
        out = out[0]
        mask = out["scores"] >= self.score_thresh
        return Detection(
            boxes=out["boxes"][mask].cpu(),
            scores=out["scores"][mask].cpu(),
            labels=out["labels"][mask].cpu(),
        )
