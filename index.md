---
title: Mapping Intertidal Elevation
---

# Mapping Intertidal Elevation from Open Satellite Data

A graduate-level, reproducible tutorial for building an **intertidal Digital Elevation
Model** — a map of the seabed that dries at low tide and floods at high tide — from open
satellite imagery (Landsat) and the global **FES2022** tide model.

The idea in one sentence: a satellite images each coastal pixel across many tide levels over
the years, so the **tide height at which a pixel switches from dry to wet is, to first order,
the elevation of the sediment surface there.** Everything here is a careful execution of that
principle.

## How this tutorial is organised

Work through the pages in order:

1. **[Setup — Environment & Installation](01_setup.md)** — install `uv`, clone the code from
   GitHub, and install all dependencies into a locked, reproducible environment.
2. **[Connecting to the Data Services](02_services.md)** — authenticate Google Earth Engine,
   or test the Planetary Computer connection.
3. **The route notebooks** — the full analysis, end to end.

## Two routes to the same result

The tutorial offers two complementary routes. They share the same FES2022 tide model and the
same physical assumptions — two implementations of one method, not two different methods.

:::{list-table}
:header-rows: 1

* - 
  - **Route 1 — Google Earth Engine**
  - **Route 2 — Planetary Computer + DEA**
* - Where it computes
  - Google's cloud (server-side)
  - Your machine (download, compute locally)
* - Account required
  - **Yes** — Google Cloud project
  - **No** — anonymous STAC access
* - Elevation algorithm
  - Transparent re-implementation (teaching)
  - The real `intertidal.elevation()` from DEA
* - Per-pixel uncertainty
  - No
  - Yes
* - Best for
  - Learning the mechanism
  - A defensible product you can cite
:::

Don't know which to pick? Use **Route 1** to learn the method quickly with no downloads, or
**Route 2** for a citable product with an uncertainty layer and no account.

---

Ready? Start with **[Setup — Environment & Installation →](01_setup.md)**.
