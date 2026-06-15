# Mapping Intertidal Elevation — Tutorial Site

Planetary Computer + DEA Intertidal + FES2022. Built with [Jupyter Book 2](https://jupyterbook.org).

## Tutorial pages (in order)

| # | File | Executable on site? |
|---|---|---|
| 1 | `01_setup.md` | No — install instructions only |
| 2 | `02_connect.ipynb` | Yes |
| 3 | `03_tides.ipynb` | Yes |
| 4 | `04_validation.ipynb` | Yes |
| 5 | `05_ndwi.ipynb` | Yes |
| 6 | `06_elevation.ipynb` | Yes |
| 7 | `07_cleanup.md` | No — uninstall / cleanup instructions only |

## Repository layout

```
.
├── myst.yml
├── index.md
├── 01_setup.md
├── 02_connect.ipynb
├── 03_tides.ipynb
├── 04_validation.ipynb
├── 05_ndwi.ipynb
├── 06_elevation.ipynb
├── 07_cleanup.md
├── cache_utils.py
├── pyproject.toml + uv.lock
├── images/
└── scripts/
```

## Run locally

```bash
uv sync --frozen
uv run jupyter lab
```

On **macOS with Anaconda**, use `./scripts/sync-env.sh` instead — it sets the system
compiler needed to build `geomad` (see `01_setup.md` Step 4).

## Build site with execution (pages 2–6)

```bash
./scripts/start-site-execute.sh    # http://localhost:3000
```

Default Jupyter token: `nck-local-execute` (printed by the script).

## Remove local install

```bash
./scripts/cleanup.sh
```

See **[7 · Cleanup](07_cleanup.md)** for details and optional steps (tide models, uv, Homebrew).
