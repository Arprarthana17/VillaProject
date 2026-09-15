# Modern Villa Dataset

Procedural Blender dataset for a 1,740 sq.ft G+1 modern villa.

## Contents

- `modern_villa_colab.py` — Google Colab runner.
- `blender/villa.py` — standalone Blender generation script.
- `metadata/dataset.json` — machine-readable dataset metadata.
- `images/` — progressive construction renders (add generated PNGs here).
- `models/` — generated OBJ/MTL/GLB files (add generated models here).

## Villa specification

- Total area: 1,740 sq.ft
- Ground floor: 870 sq.ft
- First floor: 870 sq.ft
- Configuration: G+1
- Progressive stages: 11
- Export formats: OBJ + MTL, GLB

## Run in Google Colab

1. Clone or download this repository.
2. Open `modern_villa_colab.py` in Google Colab.
3. If using the repository directly, clone it to `/content/MODERN-VILLA-DATASET`.
4. Run the script.
5. The generated dataset will be written to:
   `/content/MODERN_VILLA_1740_CLEAN`

The Blender script exports the final model as OBJ/MTL and GLB and renders 11 PNG stages.

## GitHub note

Large `.obj` and `.glb` files may exceed normal GitHub file-size limits. For large models, use Git LFS or a dataset/model-storage service rather than committing large binaries directly.
