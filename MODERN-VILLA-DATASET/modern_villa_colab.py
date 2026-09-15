# ================================================================
# MODERN VILLA DATASET - GOOGLE COLAB RUNNER
# ================================================================

import os
import sys
import subprocess
import shutil
from pathlib import Path

print("=" * 70)
print("STEP 1 - INSTALLING BLENDER")
print("=" * 70)

subprocess.run(["apt-get", "update", "-qq"], check=True)
subprocess.run(["apt-get", "install", "-y", "-qq", "blender"], check=True)

version = subprocess.run(
    ["blender", "--version"],
    capture_output=True,
    text=True,
    check=True
)
print(version.stdout.splitlines()[0])

print("=" * 70)
print("STEP 2 - INSTALLING PYTHON PACKAGES")
print("=" * 70)

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "pillow", "matplotlib"],
    check=True
)

BASE_DIR = Path("/content/MODERN_VILLA_1740_CLEAN")
if BASE_DIR.exists():
    shutil.rmtree(BASE_DIR)

IMAGE_DIR = BASE_DIR / "images"
MODEL_DIR = BASE_DIR / "model"
IMAGE_DIR.mkdir(parents=True)
MODEL_DIR.mkdir(parents=True)

# Download/copy villa.py from this repository before running this notebook,
# or upload villa.py manually into Colab.
REPO_VILLA = Path("/content/MODERN-VILLA-DATASET/blender/villa.py")
LOCAL_VILLA = Path("/content/villa.py")

if REPO_VILLA.exists():
    shutil.copy2(REPO_VILLA, LOCAL_VILLA)
elif not LOCAL_VILLA.exists():
    raise FileNotFoundError(
        "villa.py not found. Upload blender/villa.py to Colab as /content/villa.py "
        "or clone the GitHub repository first."
    )

env = os.environ.copy()
env["VILLA_BASE_DIR"] = str(BASE_DIR)

print("=" * 70)
print("STEP 3 - GENERATING VILLA")
print("=" * 70)

result = subprocess.run(
    [
        "blender",
        "--background",
        "--factory-startup",
        "--python",
        str(LOCAL_VILLA)
    ],
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

log = result.stdout
BASE_DIR.mkdir(parents=True, exist_ok=True)
with open(BASE_DIR / "blender.log", "w", encoding="utf-8") as f:
    f.write(log)

print(log)
print("BLENDER RETURN CODE:", result.returncode)

print("=" * 70)
print("STEP 4 - VERIFYING PNG FILES")
print("=" * 70)

from PIL import Image

expected = [
    "01_FOUNDATION.png",
    "02_GROUND_FLOOR.png",
    "03_FIRST_FLOOR.png",
    "04_COLUMNS.png",
    "05_WALLS.png",
    "06_SLABS.png",
    "07_STAIRCASE.png",
    "08_WINDOWS_DOORS.png",
    "09_BALCONY_ROOF.png",
    "10_FACADE_LANDSCAPE.png",
    "11_FINAL_ASSEMBLED.png"
]

valid = []

for filename in expected:
    path = IMAGE_DIR / filename

    if not path.exists():
        print("MISSING:", filename)
        continue

    try:
        with Image.open(path) as img:
            img.verify()

        size = path.stat().st_size

        if size > 5000:
            valid.append(path)
            print("OK:", filename, f"({size/1024:.1f} KB)")
        else:
            print("TOO SMALL:", filename)

    except Exception as e:
        print("INVALID:", filename, e)

print("=" * 70)
print("STEP 5 - DISPLAYING PROGRESSIVE IMAGES")
print("=" * 70)

import matplotlib.pyplot as plt

component_paths = [
    IMAGE_DIR / x
    for x in expected[:10]
    if (IMAGE_DIR / x).exists()
]

if component_paths:
    fig, axes = plt.subplots(2, 5, figsize=(22, 9))

    for i, ax in enumerate(axes.flat):
        if i < len(component_paths):
            path = component_paths[i]
            img = Image.open(path)
            ax.imshow(img)
            ax.set_title(
                path.stem.replace("_", " "),
                fontsize=11,
                fontweight="bold"
            )
        ax.axis("off")

    plt.tight_layout()
    preview_path = BASE_DIR / "10_COMPONENT_IMAGES.png"
    plt.savefig(preview_path, dpi=150, bbox_inches="tight")
    plt.show()

print("=" * 70)
print("STEP 6 - FINAL ASSEMBLED VILLA")
print("=" * 70)

final_path = IMAGE_DIR / "11_FINAL_ASSEMBLED.png"

if final_path.exists():
    try:
        final_image = Image.open(final_path)
        plt.figure(figsize=(14, 10))
        plt.imshow(final_image)
        plt.title(
            "FINAL ASSEMBLED MODERN VILLA — 1,740 SQ.FT",
            fontsize=17,
            fontweight="bold"
        )
        plt.axis("off")
        plt.show()
        print("FINAL IMAGE CREATED")
    except Exception as e:
        print("FINAL IMAGE ERROR:", e)

print("=" * 70)
print("FINAL RESULT")
print("=" * 70)

glb_path = MODEL_DIR / "VILLA_000001_MODERN.glb"
obj_path = MODEL_DIR / "VILLA_000001_MODERN.obj"
mtl_path = MODEL_DIR / "VILLA_000001_MODERN.mtl"

print(f"PNG images: {len(valid)} / 11")
print("Villa area: 1,740 sq.ft")
print("Floor area: 870 + 870 sq.ft")
print("Building: G+1 Modern Villa")
print("GLB:", "CREATED" if glb_path.exists() else "NOT CREATED")
print("OBJ:", "CREATED" if obj_path.exists() else "NOT CREATED")
print("MTL:", "CREATED" if mtl_path.exists() else "NOT CREATED")

print("Dataset location:", BASE_DIR)
print("Images:", IMAGE_DIR)
print("Models:", MODEL_DIR)
print("=" * 70)
print("DONE")
print("=" * 70)
