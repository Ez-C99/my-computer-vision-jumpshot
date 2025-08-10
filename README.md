# my-computer-vision-jumpshot

A proof-of-concept pipeline to analyse a basketball jump shot:

- **2D pose** (MMPose) – returns 17-keypoint COCO skeleton.
- **Ball/hoop detection** (YOLOX).
- **Tracking** (ByteTrack) – associate detections over time.
- **Shot segmentation** – Idle → Load → Rise → Release → Flight → Land.
- **Metrics JSON** – timings, angles, release height proxy.
- **3D avatar placeholder** – `.glb` export; later swap in VIBE→SMPL.

> Licences of key deps: **MMPose** (Apache-2.0), **YOLOX** (Apache-2.0), **ByteTrack** (MIT), **trimesh** (MIT), **three.js** (MIT).

## Quick start

1) **Python & PyTorch**
   - Create a venv and install PyTorch per the official guide for your OS/CUDA.
   - Then run the helper script below which installs OpenMMLab components via **OpenMIM** to pull the correct wheels. (This prevents common build issues.) :contentReference[oaicite:2]{index=2}

2) **Initialise the environment**

```bash
bash scripts/initialise_environment.sh

## Project Structure
```plaintext
my-copmuter-vision-jumpshot/
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
├─ LICENCE                  # Apache-2.0
├─ NOTICE                   # Attributions + third-party notices
├─ README.md
├─ Makefile
├─ pyproject.toml           # Package + dependencies (modern PEP 621)
├─ requirements-dev.txt     # Dev/test/formatting tools (optional)
│
├─ configs/
│  ├─ tracking/
│  │  └─ bytetrack.yaml     # Tracker hyperparameters (association thresholds etc.)
│  ├─ mmpose/
│  │  ├─ README.md          # Which MMPose model/config to target (e.g. RTMPose-S)
│  │  └─ rtmpose-s-body.py  # Reference to upstream config (kept as a pointer or copy notes)
│  └─ yolox/
│     ├─ README.md
│     └─ yolox_s.py         # YOLOX exp file (if customised); otherwise document weights URL
│
├─ docs/
│  ├─ OVERVIEW.md           # Problem, scope, demo GIF
│  ├─ ARCHITECTURE.md       # Modules, dataflow diagram
│  ├─ INSTALL.md            # OS-specific setup (PyTorch, MMEngine/MMCV, MMPose, YOLOX)
│  ├─ DATA_RIGHTS.md        # Guidance on personal footage vs third-party
│  └─ THIRD-PARTY-LICENCES.md
│
├─ scripts/
│  ├─ initialise_environment.sh   # Create venv, install deps, pre-commit
│  ├─ fetch_models.sh             # Guided downloader for MMPose/YOLOX weights (no redistribution)
│  ├─ prepare_examples.sh         # Grab a tiny synthetic/demo clip you own
│  └─ run_demo.sh                 # One-liner to run on a sample video
│
├─ my_computer_vision_jumpshot/               # Python package
│  ├─ __init__.py
│  ├─ cli.py                # `python -m my_computer_vision_jumpshot ...` entrypoint
│  │
│  ├─ inference/
│  │  ├─ __init__.py
│  │  ├─ pose_mmpose.py     # Wrapper: load MMPose model, return 2D keypoints
│  │  └─ detect_yolox.py    # Wrapper: load YOLOX, detect person/ball/hoop
│  │
│  ├─ tracking/
│  │  ├─ __init__.py
│  │  ├─ bytetrack_wrapper.py  # BYTETracker adapter (IDs, association)
│  │  └─ ball_association.py   # Logic to pick the basketball track among detections
│  │
│  ├─ processing/
│  │  ├─ __init__.py
│  │  ├─ features.py        # Angles, velocities, release proxies
│  │  ├─ smoothing.py
│  │  ├─ shot_fsm.py        # Idle→Load→Rise→Release→Flight→Land
│  │  └─ metrics.py         # Per-shot JSON metrics
│  │
│  ├─ io/
│  │  ├─ __init__.py
│  │  ├─ renderer.py        # OpenCV overlays to MP4
│  │  ├─ serialise.py       # British spelling; write/read JSON, YAML
│  │  ├─ mesh_export.py     # Placeholder GLB; later VIBE→SMPL export
│  │  └─ video_utils.py     # FPS, frame seeking, safe decode
│  │
│  ├─ web/
│  │  └─ viewer.html        # three.js GLB viewer for avatar preview
│  │
│  └─ data_schemas/
│     ├─ metrics.schema.json
│     └─ tracks.schema.json
│
├─ data/
│  ├─ raw/.gitkeep
│  ├─ processed/.gitkeep
│  └─ models/.gitkeep        # (empty; weights fetched by scripts, gitignored)
│
├─ examples/
│  ├─ sample_video.mp4       # Tiny owned/synthetic clip or leave README.txt instead
│  └─ sample_output/
│     ├─ metrics.json
│     ├─ shot_00.mp4
│     └─ avatar_placeholder.glb
│
├─ notebooks/
│  └─ exploration.ipynb      # Optional: quick EDA, visual checks
│
└─ tests/
   ├─ __init__.py
   ├─ test_metrics.py
   ├─ test_shot_fsm.py
   └─ test_serialise.py

```
