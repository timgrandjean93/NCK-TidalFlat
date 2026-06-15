---
title: 7 · Cleanup — undo the installation
short_title: 7 · Cleanup
execute:
  skip: true
---

# 7 · Cleanup — undo the installation

### Remove everything the tutorial created on your computer

This page reverses **[1 · Setup](01_setup.md)** and the notebook runs. Nothing here deletes
your GitHub account, Planetary Computer access, or anything on Microsoft's servers — only
**local files and settings** on your machine.

**Previous:** [6 · Elevation](06_elevation.ipynb)

---

## What the tutorial added locally

| Item | Location | Size (typical) | Safe to delete? |
|---|---|---|---|
| Python environment | `.venv/` | 1–3 GB | Yes |
| Downloaded scene / tide caches | `cache/` | 0.1–10+ GB | Yes |
| FES2022 tide model files | `tide_models/` | ~1 GB | Yes (keep if you reuse later) |
| Notebook figures | `*.png` in repo root | MB each | Yes |
| GeoTIFF / NetCDF exports | `*.nc`, `*.tif` | MB–GB | Yes |
| Landsat NDWI year caches | `cache/elevation_*/` | GB | Yes |
| Jupyter kernel | `nck` (user install) | tiny | Yes |
| Built website preview | `_build/` | varies | Yes |
| Tutorial source code | repo folder | small | Only if you remove the whole clone |

---

## Quick cleanup (recommended)

From the **repository root**, with Jupyter stopped:

```bash
chmod +x scripts/cleanup.sh   # once
./scripts/cleanup.sh
```

This removes `.venv/`, `cache/`, notebook outputs in the repo root, `_build/`, and the
`nck` Jupyter kernel. It does **not** delete `tide_models/` or the repository itself.

---

## Step-by-step (manual)

### Step 1 — Stop running servers

Quit **Jupyter Lab**, **Jupyter Book preview** (`jupyter book start`), and any notebook
kernels that still show `nck` as busy.

### Step 2 — Remove the Jupyter kernel

Do this **before** deleting `.venv/` (the uninstall command needs a working environment):

```bash
uv run jupyter kernelspec uninstall nck
```

Confirm with `y` when prompted. If `.venv` is already gone:

```bash
jupyter kernelspec list
jupyter kernelspec uninstall nck
```

### Step 3 — Remove the Python environment

```bash
rm -rf .venv
```

This removes all packages (`dea-intertidal`, `geomad`, `llvmlite`, etc.). Your system
Python and Anaconda (if installed) are untouched.

### Step 4 — Remove caches and notebook outputs

```bash
rm -rf cache/
rm -f ./*.png ./*.nc ./*.tif
rm -rf _build/ .ipynb_checkpoints/
```

To also remove **Zarr** folders if any were created outside `cache/`:

```bash
find . -maxdepth 2 -name '*.zarr' -type d -exec rm -rf {} +
```

### Step 5 — Tide model (optional)

Only if you do not need FES2022 again:

```bash
rm -rf tide_models/
```

### Step 6 — Remove the repository (optional)

To delete the **entire tutorial** including notebooks:

```bash
cd ..
rm -rf NCK-TidalFlat
```

Use your actual folder name if you renamed the clone.

---

## Optional — undo global tools

Only if you installed these **for this course** and want them gone completely.

| Tool | Remove |
|---|---|
| **jupyter-book** (uv tool) | `uv tool uninstall jupyter-book` |
| **Python 3.12 via uv** | `uv python uninstall 3.12` |
| **uv itself** | `rm -rf ~/.local/bin/uv` and remove uv from your shell profile (see [uv docs](https://docs.astral.sh/uv/)) |
| **libomp** (macOS, OpenMP) | `brew uninstall libomp` |
| **Homebrew** | Usually **keep** — other apps may use it. Uninstall only if you know you do not need it: see [brew.sh FAQ](https://docs.brew.sh/FAQ#how-do-i-uninstall-homebrew) |

We do **not** recommend uninstalling Xcode Command Line Tools or Homebrew unless you are
sure nothing else on your Mac depends on them.

---

## Verify cleanup

From the repo root (after `./scripts/cleanup.sh`):

```bash
test ! -d .venv && echo "OK: .venv gone"
test ! -d cache && echo "OK: cache gone"
jupyter kernelspec list | grep -q nck && echo "WARN: nck kernel still present" || echo "OK: nck kernel gone"
```

To start fresh later, return to **[1 · Setup](01_setup.md)** and run `./scripts/sync-env.sh`
again.

---

**You finished the tutorial chain:**

Setup → Connect → Tides → Validation → NDWI → Elevation → **Cleanup**
