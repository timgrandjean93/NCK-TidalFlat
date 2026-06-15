# Mapping Intertidal Elevation — Two Routes

This tutorial maps the elevation of an intertidal flat (the zone that dries at low tide and
floods at high tide) from open satellite imagery and a global tide model. It comes in **two
self-contained routes**. They produce the same kind of product but take fundamentally different
paths — pick one, or teach both to contrast them.

Each route lives in its own folder with its own pinned, locked environment, because their
dependency trees genuinely conflict and must not share one environment.

```
intertidal-tutorial/
├── README.md                ← you are here
├── gee/                     ← Route 1: Google Earth Engine
│   ├── intertidal_elevation_GEE_tutorial.ipynb
│   ├── pyproject.toml + uv.lock        (uv environment)
│   └── environment.yml + requirements.txt   (conda fallback)
└── pc/                      ← Route 2: Planetary Computer + DEA Intertidal
    ├── intertidal_elevation_PC_tutorial.ipynb
    └── pyproject.toml + uv.lock
```

---

## Which route should I use?

| | **Route 1 — GEE** (`gee/`) | **Route 2 — Planetary Computer + DEA** (`pc/`) |
|---|---|---|
| Where computation happens | Google's cloud (server-side) | **Your machine** (download, compute locally) |
| **Account required** | **Yes** — Google Cloud project + one-time auth | **No** — STAC + Landsat/Sentinel-2 are anonymous |
| Elevation algorithm | A transparent re-implementation (teaching) | **The real `intertidal.elevation()`** from DEA |
| Uncertainty layer | No | **Yes**, per pixel |
| Tide model | FES2022 (via `eo-tides`) | FES2022 (via `eo-tides`) — identical |
| Scales to large areas | Easily (no download) | Limited by your bandwidth + memory |
| Best for | Learning the *mechanism*; quick exploration | A *defensible product* you can cite |

Both routes share the **same tide model and the same physical assumptions**, so they are two
implementations of one method, not two different methods. The Planetary Computer "account
question": the STAC catalogue and core open collections are anonymously accessible;
`planetary_computer.sign()` works **without a key**. A free key only raises rate limits / unlocks
some premium datasets (e.g. Sentinel-1 RTC) and is **not** needed for the optical workflow here.

---

## One-time prerequisite for BOTH routes: the FES2022 tide model

Earth Engine and Planetary Computer both lack sea-level-at-acquisition-time, so both routes need
the FES2022 tide model on disk (you can share one copy between them).

Obtain it (free, with registration) from **AVISO+**:
https://www.aviso.altimetry.fr/en/data/data-access/registration-form.html — request the
**FES (Finite Element Solution) tide** product, then arrange the constituent files as:

```
tide_models/
└── fes2022b/
    └── ocean_tide/
        ├── m2_fes2022.nc
        ├── s2_fes2022.nc
        └── ...   (~34 constituents)
```

Point each notebook's `TIDE_DIR` at this folder. (This step is manual because AVISO requires an
authenticated download.)

---

## Install uv (both routes use it)

`uv` is a fast, modern Python project manager. One command installs a self-contained binary —
it does not need a pre-existing Python:

- **macOS / Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Reopen your terminal, then check: `uv --version`.

You do **not** need to install GDAL yourself — it ships inside the `rasterio`/`pyogrio` wheels.

---

## Running Route 1 — GEE

```bash
cd gee
uv sync --frozen          # Python 3.12 + the exact locked package set
uv run jupyter lab        # open intertidal_elevation_GEE_tutorial.ipynb
```

You will also need a (free) Earth Engine account; the notebook walks you through the one-time
authentication. A conda fallback (`environment.yml`) is provided in `gee/` for restricted
networks where uv cannot download Python.

## Running Route 2 — Planetary Computer + DEA

```bash
cd pc
uv sync --frozen          # Python 3.12 + the exact locked package set
uv run jupyter lab        # open intertidal_elevation_PC_tutorial.ipynb
```

No account needed. Note this environment is pinned carefully: `dea-intertidal` requires an older
`rasterio`, which forces `eodatasets3==1.9.3` (the latest pulls a newer `datacube` that
conflicts). The lock file captures the verified, working tree — `uv sync --frozen` reproduces it
exactly.

---

## Reproducibility

Each route's `uv.lock` records the full resolved dependency tree, pinned to exact versions. A
colleague running `uv sync --frozen` later gets a byte-for-byte identical environment. After
setup, each notebook's Stage 0 prints the resolved versions for your methods / supplementary
information.

## Verified

Both environments were resolved and their key imports tested (June 2026), including a successful
import of `intertidal.elevation` in the `pc` environment. As a final check before distributing,
run `uv sync --frozen` once on macOS and Windows to confirm the cross-platform wheels resolve.
