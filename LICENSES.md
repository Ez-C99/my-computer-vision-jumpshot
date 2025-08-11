# Licences for `my-computer-vision-jumpshot`

This project is licensed under **Apache License 2.0** (SPDX: Apache-2.0). See `LICENSE` at the repo root.

> ⚠️ Notes you should be aware of:
>
> - **OpenMMLab libraries (MMDetection, MMPose, MMCV, MMEngine)** are Apache-2.0, but **some specific ops/components in MMCV carry other licences**. Check their `LICENSES.md` before enabling optional CUDA/ops you don’t need for CPU/macOS.  
> - **Model weights** and **datasets** may have their own terms even if the code is permissive. Review them before redistribution or commercial use.

## 1) Core Python components

| Component | Purpose | Version | Licence | Source |
|---|---|---:|---|---|
| **PyTorch** | DL framework | `<pin>` | BSD-3-Clause | https://github.com/pytorch/pytorch/blob/main/LICENSE |
| **MMEngine** | Training/runtime | `<pin>` | Apache-2.0 | https://github.com/open-mmlab/mmengine/blob/main/LICENSE |
| **MMCV / mmcv-lite** | CV foundation | `<pin>` | Apache-2.0 *(plus exceptions; see MMCV `LICENSES.md`)* | https://github.com/open-mmlab/mmcv |
| **MMDetection** | Object detection (RTMDet) | `<pin>` | Apache-2.0 | https://github.com/open-mmlab/mmdetection/blob/main/LICENSE |
| **MMPose** | Pose estimation | `<pin>` | Apache-2.0 | https://github.com/open-mmlab/mmpose/blob/main/LICENSE |
| **OpenMIM** | Installer for MM* | `<pin>` | Apache-2.0 | https://github.com/open-mmlab/mim |
| **Supervision** | Tracking helpers (ByteTrack wrapper, viz) | `<pin>` | MIT | https://github.com/roboflow/supervision/blob/main/LICENSE.md |
| **ByteTrack (algorithm)** | Multi-object tracking | `<pin>` | MIT | https://github.com/ifzhang/ByteTrack/blob/main/LICENSE |

**Sources:** PyTorch license (BSD-3) confirms permissive use, including commercial.   MMDetection, MMPose, MMEngine and MMCV declare Apache-2.0; MMCV also flags extra-licensed ops in its `LICENSES.md` (check that file if you flip features on). OpenMIM is Apache-2.0. Supervision is MIT, and the original ByteTrack repo is MIT.

## 2) Web/3D runtime (for the demo viewer)

Pick one of the renderers below—both are permissive and production-proven:

| Component | Purpose | Licence | Source |
|---|---|---|---|
| **three.js** | WebGL renderer, loaders | MIT | https://github.com/mrdoob/three.js/blob/dev/LICENSE |
| **Babylon.js** | WebGL renderer/engine | Apache-2.0 | https://github.com/BabylonJS/Babylon.js/blob/master/LICENSE.md |
| **Filament (optional)** | Physically-based rendering | Apache-2.0 | https://github.com/google/filament/blob/main/LICENSE |
| **glTF 2.0 (format)** | Asset interchange | Royalty-free standard (Khronos) | https://www.khronos.org/gltf/ |

**Sources:** three.js (MIT), Babylon.js (Apache-2.0), Filament (Apache-2.0), glTF is a royalty-free standard maintained by Khronos.

## 3) Models, weights and datasets

- **Pretrained weights** from OpenMMLab model zoos are generally under the same licence as the code, but always confirm the specific model card. MMCV’s repo explicitly notes extra licences for certain ops.
- **COCO**: image copyrights vary; **annotations** are **CC BY 4.0**. For commercial redistribution, you must respect attribution and the underlying image owners’ terms.
- **CrowdHuman**: dataset code repo is **MIT**; some distributions also note **CC BY 4.0** on mirrors—verify the source you download from.

## 4) How to regenerate this file automatically

From your project venv:

```bash
pip install -U pip-licenses
pip-licenses \
  --from=mixed \
  --with-urls --with-authors \
  --format=markdown \
  --output-file LICENSES.generated.md
````

* `pip-licenses` documents options to include license texts and NOTICE files if you want a single combined artefact; pair with `--with-license-file` and `--with-notice-file` (best with `--format=json`). ([PyPI][1])

## 5) Version pins (fill as you lock them)

```plaintext
torch==<x.y.z>
mmengine==<x.y.z>
mmcv-lite==<x.y.z>
mmdet==<x.y.z>
mmpose==<x.y.z>
openmim==<x.y.z>
supervision==<x.y.z>
```
