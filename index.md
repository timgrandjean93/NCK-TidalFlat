---
title: Mapping Intertidal Elevation
---

# Mapping Intertidal Elevation from Open Satellite Data

This is a graduate-level, reproducible tutorial for building an **intertidal Digital
Elevation Model (DEM)** — a map of the elevation of the seabed that dries at low tide and
floods at high tide — using only open satellite imagery and a global tide model.

The physical idea in one sentence: a satellite images each coastal pixel across many
different tide levels over the years, so the **tide height at which a pixel switches from
dry to wet is, to first order, the elevation of the sediment surface there.** Everything
in this tutorial is a careful execution of that principle.

The tutorial provides **two complementary routes** to the same kind of result. They share
the same FES2022 tide model and the same physical assumptions, so they are two
implementations of one method — not two different methods.

:::{list-table} Choosing a route
:header-rows: 1

* - 
  - **Route 1 — Google Earth Engine**
  - **Route 2 — Planetary Computer + DEA**
* - Where computation happens
  - Google's cloud (server-side)
  - Your machine (download, compute locally)
* - Account required
  - **Yes** — Google Cloud project + auth
  - **No** — STAC + Landsat are anonymous
* - Elevation algorithm
  - Transparent re-implementation (teaching)
  - The real `intertidal.elevation()` from DEA
* - Per-pixel uncertainty
  - No
  - Yes
* - Scales to large areas
  - Easily (no download)
  - Limited by bandwidth + memory
* - Best for
  - Learning the mechanism; quick exploration
  - A defensible product you can cite
:::

## How to use this site

Each route is a Jupyter notebook you can read here in full, then download and run yourself.
The notebooks are shown **as written** — they are not executed on this website, because
they require interactive Earth Engine authentication, a registered tide-model download, and
local data that cannot run on a build server. You run them in your own environment by
following the setup below.

:::{note} One-time prerequisite for both routes: the FES2022 tide model
Both routes need the FES2022 tide model on disk (one shared copy is fine). Obtain it (free,
with registration) from [AVISO+](https://www.aviso.altimetry.fr/en/data/data-access/registration-form.html),
requesting the **FES tide** product, and arrange the constituent files as
`tide_models/fes2022b/ocean_tide/*.nc`. This step is manual because AVISO requires an
authenticated download.
:::

## Setting up an environment

Both routes use [`uv`](https://docs.astral.sh/uv/), a fast modern Python project manager.
Install it once:

- **macOS / Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Then, for whichever route you want, from its folder:

```bash
cd gee      # or: cd pc
uv sync --frozen      # installs Python 3.12 + the exact locked package set
uv run jupyter lab    # opens the notebook
```

The two routes have **separate, locked environments** on purpose: their dependency trees
conflict (the DEA route pins an older `rasterio`, which the GEE route does not want), so
they must not share one environment. Each `uv.lock` reproduces a byte-for-byte identical
environment for anyone, which is what makes the workflow reproducible for a methods section.

You do **not** need to install GDAL yourself — it ships inside the package wheels.

## What you will produce

By the end of either route you will have an intertidal elevation surface for a coastal area
of your choosing, exported as GeoTIFF/NetCDF, plus (in Route 2) a per-pixel uncertainty
layer. The notebooks close with an honest discussion of the method's limitations — tidal
sampling bias, datum, morphological stationarity — and how to validate the result against an
independent DEM.
