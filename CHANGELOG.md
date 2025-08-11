# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [Unreleased]

- First runnable end-to-end demo CLI (detect → pose → track → metrics).
- Optional 2D→3D lift with VideoPose3D adapter.
- Ball/hoop detection upgrade path (fine-tune small detector on custom clips).

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
