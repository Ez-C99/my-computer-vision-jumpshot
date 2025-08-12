# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [Unreleased]

### Planned

- **A – Metrics pass:** Add per-shot kinematics (e.g., wrist/elbow angles, release timing proxy) and write to `metrics.json`.
- **B – TorchVisionDetector:** Optional person/hoop/ball regions to crop pose input and seed ball candidates for tracking.
- **C – Ball tracking (Norfair):** Simple Kalman-based tracker for ball trajectory; derive release/flight metrics.
- **D – 2D→3D lift (VideoPose3D):** Integrate lifting for 3D joints and basic kinematic features (segment angles, angular velocities).

---

## [0.1.1] - 2025-08-12

### Added

- **MediaPipe pose wrapper** (`my_computer_vision_jumpshot/inference/pose_mediapipe.py`) returning 33-landmark skeleton; basic adapters and typing.
- **Norfair tracking wrapper** (`tracking/norfair_wrapper.py`) with config stub and association scaffolding.
- **CLI scaffolding** (`my_computer_vision_jumpshot/cli.py`) and smoke tests for imports.
- **IO utilities** (`io/video_utils.py`, `io/serialise.py`) for safe video decode and JSON/YAML helpers.
- **Scripts:** `scripts/initialise_environment.sh`, `scripts/fetch_third_party.sh`, `scripts/prepare_examples.sh`.
- **Docs:** Updated `README.md` with step-by-step install/run; project structure aligned to the new stack.

### Changed

- **Dependencies pinned for easy install:** `torch==2.2.2`, `torchvision==0.17.2`, `mediapipe==0.10.14`. Resolved Norfair/Rich conflict by pinning **`rich==12.6.0`** (Norfair requires `<13`).
- **Third-party:** Cloned `third_party/VideoPose3D` (commit to be pinned after first successful run).

### Fixed

- **Dependency resolution issues** (Norfair vs Rich) and **Torch/TorchVision version mismatch** on pip.

### Notes

- The stack remains **pure-pip, CPU-friendly** (no compiled-ops like MMCV), to keep the PoC unblocked.
- Detection is currently optional; TorchVision detectors will be introduced in the next iteration (see “Planned”).

## [0.1.0] - 2025-08-11

### Changed

- **Stack pivot for PoC velocity:** From MMDetection (YOLOX + MMPose + ByteTrack) to a pure-pip, CPU-friendly stack:
  - **TorchVision** detectors (RetinaNet / Faster R-CNN, COCO weights).
  - **MediaPipe BlazePose** for 2D pose (33 landmarks).
  - **Norfair** for simple multi-object tracking (MIT).
  - **VideoPose3D** vendored as third_party for optional 2D→3D lifting (MIT).
- Updated `README.md`, project structure, and `requirements.txt` to reflect the new stack.

### Added

- `third_party/VideoPose3D` clone instructions and import smoke test.
- Config stubs under `configs/{detection,pose,tracking,lift,action}`.
- CPU-only macOS install path; avoids native C++/CUDA extension builds.

### Rationale

- **Why the change?** Building **mmcv** / compiled ops on macOS (Intel) failed during C++ extension compile (`fatal error: 'mutex' file not found` and related toolchain issues). For a fast PoC, we chose a stack that installs from wheels without bespoke compilers or CUDA.
- **Future path:** MMDetection remains an option later. With a Linux box (or container with GPU), MMDetection + MMPose can be reintroduced for broader model coverage. The current module boundaries (detect/pose/track/lift) make migration straightforward.

### Known limitations

- Ball/hoop detection is heuristic at first; expect a later fine-tuned small detector.
- MediaPipe’s skeleton differs from COCO’s 17-keypoint layout; conversion utils will be added if needed.

## [0.0.3] - 2025-08-10

### Changed

- Initial plan: **MMDetection**-based stack (YOLOX for detection, MMPose for pose, ByteTrack for tracking).
- Began macOS setup; pinned configs and tried to fetch YOLOX weights via `mim`.

### Issues Encountered

- `mmcv` wheel build failed on macOS during extension compilation (C++17/stdlib/Xcode CLT headers).
- Given no Linux machine available and containerized GPU not feasible locally, setup blocked PoC progress.
