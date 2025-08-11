# my-computer-vision-jumpshot

A proof-of-concept pipeline to analyse a basketball jump shot:

- **Person detection** (TorchVision RetinaNet / Faster R-CNN; COCO-pretrained).
- **2D pose** (MediaPipe BlazePose) – 33 body landmarks (plus visibility).
- **Tracking** (Norfair, MIT) – simple, CPU-friendly ID association.
- **(Early) ball/hoop cues** – heuristics to start; model fine-tune later.
- **Shot segmentation** – Idle → Load → Rise → Release → Flight → Land.
- **Metrics JSON** – timings, angles, release height proxy.
- **3D avatar placeholder** – `.glb` export; later swap in VIBE→SMPL.

> Licences of key deps: **PyTorch/TorchVision** (BSD-style), **MediaPipe** (Apache-2.0),
**Norfair** (MIT), **VideoPose3D** (MIT), **trimesh** (MIT), **three.js** (MIT).

## Quick start

> **Compatibility:** This PoC targets macOS (Intel) with CPU-only PyTorch wheels.
> It also runs on Apple Silicon (MPS) with the matching Torch/TorchVision wheels.
> No CUDA required. If you later move to Linux + GPU, model choices stay the same.

### 1. **Python Virtual Environment**

- Create a Python 3.11 venv and activate.

```bash
python3.11 -m venv .venv

source .venv/bin/activate
python --version    # sanity check
```

### 2. **Fetch third-party code (VideoPose3D)**

```bash
# create the third_party folder if missing
mkdir -p third_party

# clone VideoPose3D (shallow); we’ll pin the exact commit after we test it locally
git clone --depth 1 https://github.com/facebookresearch/VideoPose3D.git third_party/VideoPose3D

# (optional) record the commit you got today, so we can pin it later if needed
git -C third_party/VideoPose3D rev-parse --short HEAD
```

> Note: I deliberately didn’t “git checkout” a hardcoded hash so we don’t risk a nonexistent commit. Once we run it, we’ll pin the exact commit you pulled (just drop it in a `third_party/LOCKFILE.txt` later).

### 3. Create example/output + models folders

```bash
mkdir -p examples/sample_output data/models
```

If you don’t already have a tiny test video:

- put one you own at `examples/sample_video.mp4`, or
- rename whatever short clip you have to that path.

### 4. Quick smoke tests (imports)

Make sure the big pieces load:

```bash
python - <<'PY'
import torch, cv2, mediapipe as mp
print("torch:", torch.__version__)
print("opencv:", cv2.__version__)
print("mediapipe:", mp.__version__)
print("✅ core imports OK")
PY
```

And that VideoPose3D can be imported from `third_party`:

```bash
python - <<'PY'
import sys
sys.path.append('third_party/VideoPose3D')
import common.model as vp3d_model  # core module
print("✅ VideoPose3D import OK")
PY
```

## Project Structure

```plaintext
my-computer-vision-jumpshot/
├─ .github/
│  ├─ ISSUE_TEMPLATE.md
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ workflows/
│     └─ ci.yml
├─ .gitignore
├─ .gitattributes
├─ .pre-commit-config.yaml
├─ .env.example
├─ CHANGELOG.md
├─ CITATION.cff
├─ CODE_OF_CONDUCT.md
├─ CONTRIBUTING.md
├─ LICENCE                  # Apache-2.0 (project)
├─ NOTICE                   # Attributions + third-party notices
├─ README.md
├─ Makefile
├─ pyproject.toml          
├─ requirements.txt         # <-- new stack deps (runtime)
├─ requirements-dev.txt     # linters/formatters/tests (optional)
│
├─ configs/
│  ├─ detection/
│  │  └─ torchvision_retinanet.yaml
│  ├─ pose/
│  │  └─ mediapipe_pose.yaml
│  ├─ tracking/
│  │  └─ norfair.yaml
│  ├─ lift/
│  │  └─ videopose3d.yaml
│  └─ action/
│     └─ stgcn.yaml         # skeleton-based action model (placeholder to start)
│
├─ docs/
│  ├─ OVERVIEW.md
│  ├─ ARCHITECTURE.md
│  ├─ INSTALL.md            # macOS steps for this stack (below)
│  ├─ DATA_RIGHTS.md
│  └─ THIRD-PARTY-LICENCES.md
│
├─ scripts/
│  ├─ initialise_environment.sh
│  ├─ fetch_third_party.sh  # pulls VideoPose3D (and pins a commit)
│  ├─ prepare_examples.sh
│  └─ run_demo.sh
│
├─ third_party/
│  └─ VideoPose3D/          # vendored clone (MIT)
│
├─ my_computer_vision_jumpshot/               # Python package
│  ├─ __init__.py
│  ├─ cli.py                # `python -m my_computer_vision_jumpshot ...`
│  │
│  ├─ inference/
│  │  ├─ __init__.py
│  │  ├─ detect_torchvision.py   # RetinaNet/Faster R-CNN wrapper
│  │  └─ pose_mediapipe.py       # 2D pose (33 landmarks)
│  │
│  ├─ tracking/
│  │  ├─ __init__.py
│  │  └─ norfair_wrapper.py      # ID tracking; ball/hoop association helpers
│  │
│  ├─ lift3d/
│  │  ├─ __init__.py
│  │  └─ videopose3d_adapter.py  # 2D→3D lifting bridge to third_party/VideoPose3D
│  │
│  ├─ action/
│  │  ├─ __init__.py
│  │  └─ stgcn.py                # placeholder/simple baseline on keypoints
│  │
│  ├─ processing/
│  │  ├─ __init__.py
│  │  ├─ features.py             # angles, velocities, release timing
│  │  ├─ smoothing.py
│  │  ├─ shot_fsm.py             # Idle→Load→Rise→Release→Flight→Land
│  │  └─ metrics.py              # per-shot JSON
│  │
│  ├─ io/
│  │  ├─ __init__.py
│  │  ├─ renderer.py             # overlays to MP4
│  │  ├─ serialise.py
│  │  └─ video_utils.py
│  │
│  ├─ web/
│  │  └─ viewer.html
│  │
│  └─ data_schemas/
│     ├─ metrics.schema.json
│     └─ tracks.schema.json
│
├─ data/
│  ├─ raw/.gitkeep
│  ├─ processed/.gitkeep
│  └─ models/.gitkeep        # weights/artifacts, gitignored
│
├─ examples/
│  ├─ sample_video.mp4
│  └─ sample_output/
│     ├─ metrics.json
│     ├─ shot_00.mp4
│     └─ avatar_placeholder.glb
│
├─ notebooks/
│  └─ exploration.ipynb
│
└─ tests/
   ├─ __init__.py
   ├─ test_metrics.py
   ├─ test_shot_fsm.py
   └─ test_serialise.py
```
