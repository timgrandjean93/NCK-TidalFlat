---
title: Applications & next steps
short_title: Applications
execute:
  skip: true
---

# Applications & next steps

You have finished the **six tutorial pages**. The last one — **[6 · Elevation](06_elevation.ipynb)** —
produced an elevation map for one area and one time window. Treat that as a **starting point**,
not the end product.

From here, you work **as a group** on the Wadden Sea: formulate your own **research question**
and **hypotheses**, and explore them over the next few days. This page sketches what
satellite-derived intertidal elevation is good for, and how it compares to traditional surveys.

**Previous:** [6 · Elevation](06_elevation.ipynb)

---

## One map — or a time series?

Page 6 gives you **height (m, MSL) per pixel** for a chosen period (e.g. 2023–2025). The
tutorial uses **Landsat only** (30 m, long archive). You can extend the same logic in
several directions:

| Approach | What you get |
|---|---|
| **Single window** (page 6) | One DEM + uncertainty + QA layers |
| **Multiple windows** | Elevation at t₁, t₂, t₃, … → change maps (Δ*z*) |
| **Long archive** (Landsat from ~1984) | Decadal context — if tide sampling is adequate |
| **Add Sentinel-2** *(advanced)* | Denser revisit (~5 d) and 10 m bands — not in the tutorial notebook, but useful for shorter epochs or sharper spatial detail if you harmonise to one grid |

Run page 6 again with a different `START` / `END` to build another **epoch**. Stack several
epochs and you have a **time series of elevation surfaces** — a natural way to study
morphological trends in the Wadden Sea.

The method does not measure height on a single day. It **integrates** many satellite passes
tagged with modelled tide height. A three-year window is a practical compromise; shorter
windows are noisier, longer windows assume morphology is stable.

---

## Satellite vs. LiDAR — why the temporal gap matters

**Airborne LiDAR** (and vessel surveys) remain the accuracy benchmark on tidal flats.
In the Netherlands, wide-area **Waddenzee** LiDAR runs on the order of **once every five
years**; the **Westerschelde** is surveyed more often, but still in discrete campaigns.
Between campaigns the surface moves — channels shift, flats accrete or erode, marsh edges
advance or retreat — and you only see those changes when the next survey lands.

**Satellite intertidal elevation** trades some vertical precision for **repeatability**:

| | LiDAR / survey vessel | Satellite (this tutorial) |
|---|---|---|
| **Vertical accuracy** | cm-scale (when well controlled) | dm-scale (typical; use QA layers) |
| **Horizontal resolution** | dm–m (LiDAR) | 30 m (Landsat); 10 m possible with Sentinel-2 |
| **Revisit** | Campaign-based (years) | Every clear overpass (weeks–months) |
| **Coverage** | Flight lines / project area | Any cloud-free coastal AOI globally |
| **Cost** | High per campaign | Open data + local compute |

You can build **annual or sub-annual elevation epochs** where enough clear scenes sample
the tidal range. That makes satellite data strong for:

- **Accretion and erosion rates** on flats and marsh surfaces
- **Channel migration** and bar dynamics between LiDAR cycles
- **Event response** — did a storm winter leave a detectable signal before the next survey?

Always report **uncertainty** (`elevation_uncertainty`, QA layers from page 6) and validate
against LiDAR or levelling where possible.

---

## Ecological and coastal monitoring

Elevation is a **master variable** on intertidal flats: it controls inundation time, wave
exposure, and salinity stress. Many ecological patterns follow height above sea level.

### Habitat and zonation

| Elevation band (typical) | Physical setting | Ecological relevance |
|---|---|---|
| **Upper flat / marsh edge** | Rarely inundated | Salt-marsh vegetation, pioneer zones |
| **Mid flat** | Regular wetting and drying | Benthic community transitions (e.g. mud vs sand fauna) |
| **Lower flat** | Long inundation | Higher productivity, different species pools |
| **Channels & subtidal** | Permanent water | Outside intertidal DEM — NDWI always “wet” |

Clip your elevation map to **management or monitoring units** and summarise mean height,
intertidal area, or area within elevation bins — useful for **Natura 2000** reporting,
carrying capacity studies, or benthos–elevation relationships.

### Monitoring height development

Subtract elevation at time *t₂* from *t₁* (after aligning grids and masking poor QA):

```
Δz = elevation(t₂) − elevation(t₁)
```

Positive Δ*z* → net accretion; negative → erosion. Combine with:

- **Marsh edge vectors** — is the green–bare transition moving landward or seaward?
- **Storm years** — compare windows before/after a known winter
- **Human interventions** — nourishment, dredging, depramming

At 30 m resolution you will not resolve small creek networks; combine with higher-res
imagery or field transects for detail.

### Linking to field data

Satellite elevation is most convincing when tied to **in situ** observations:

- Elevation rods / RTK-GPS along transects
- Benthic sampling
- Vegetation disitribution
- Existing LiDAR for calibration in the same epoch

---

## Directions for your group project

A few practical starting points — pick what fits your research question:

1. **Sub-regions** — clip to a shapefile (e.g. RWS **kombergingen**, Natura sites) and
   compute zonal statistics per polygon (`geopandas`, `rioxarray`, or QGIS).
2. **Multi-epoch change** — run page 6 for two or three date windows; map Δ*z* and mask
   poor QA pixels.
3. **Elevation classes** — bin heights (e.g. every 25 cm between LAT and HAT) and relate
   to ecology or management categories.
4. **Feasibility first** — revisit page 3 for tidal sampling before committing to a new AOI
   or sensor mix.

---

## Keep in mind

Remote-sensing elevation is powerful but easy to **over-interpret**. These assumptions matter:

| Check | Why |
|---|---|
| **Tidal sampling** (pages 3 & 6) | Poor HOT/LOT coverage → biased heights at range edges |
| **QA layers** (page 6, Step 9) | Mask low correlation or low clear-count pixels |
| **Datum** | FES2022 = MSL; Dutch comparisons may need NAP offset (page 4) |
| **Stability assumption** | Multi-year windows assume no major morphological overhaul |
| **Resolution** | 30 m (Landsat) — do not over-interpret creek-scale features |