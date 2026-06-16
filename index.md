---
title: Mapping Intertidal Elevation from Open Satellite Data
short_title: Home
execute:
  skip: true
---

# Background

Tidal flats are surveyed regularly, but not frequently enough. The Westerschelde is mapped every year; the Waddenzee is once every five years per tidal basin; many estuaries worldwide are far less often than that. Each survey — by vessel or aircraft — is expensive and logistically demanding, capturing a single snapshot of a surface that can shift by metres within a season. The result is a monitoring record full of gaps, in a landscape that never stops moving.

Satellites offer a different approach. They already pass over every coastal flat hundreds of times per decade, at no additional cost. Rather than sending a survey team to the tidal flat, we let those overpasses do the measuring — turning an irregular, costly survey into a continuous, free, and globally consistent one.

### The core idea

A satellite images the same coastal pixel across many different tide levels over the years. Sort those observations by the water level at the moment of acquisition, and a pattern emerges: at low water, the pixel is dry, at high water, it is wet, and somewhere in between, it flips. That crossover water level is, to first order, the elevation of the sediment surface. Repeat for every pixel, and you have an intertidal Digital Elevation Model. Everything that follows in this tutorial is a careful execution of that single principle.

The idea is simple; making it trustworthy is the work. Four things stand in the way:

1. **Tide height**. A satellite records light, not water level. We obtain the water level at acquisition time from a global harmonic tide model (FES2022), which also allows us to hindcast back to the 1980s, enabling decade-scale change detection.

2. **Wet or dry**. We detect whether a pixel is covered by water using the Normalised Difference Water Index (NDWI), computed from the green and near-infrared bands of each scene. Water absorbs near-infrared strongly; dry sediment does not.

3. **Cloud and noise**. No single image can be trusted. Instead, we accumulate many clear observations over a multi-year window, masking cloud, shadow, and sensor noise per scene before combining them.

4. **Tidal sampling bias**. A pixel's elevation can only be recovered if it was observed both below and above its crossover water level. If every clear image happened to catch high water, the low flats are never seen dry — and their elevation remains unknown.

### What this looks like

The tutorial site uses the **Wadden Sea** as its worked example. Three views of the same idea:

```{figure} images/home/ndwi_low_high.png
:label: fig-ndwi-home
:width: 100%
:alt: RGB, NDWI, and wet mask at low and high tide

**Wet vs dry (page 5).** Clear-sky Landsat scenes at opposite tides — RGB, NDWI map, and wet mask side by side.
```

```{figure} images/home/tidal_sampling_elevation.png
:label: fig-tides-home
:width: 100%
:alt: FES2022 tide curve with Landsat acquisition dots

**Tidal sampling (page 6).** Each Landsat overpass tagged with FES2022 tide height — the same heights used in the elevation fit.
```

```{figure} images/home/elevation_map.png
:label: fig-elev-home
:width: 100%
:alt: Intertidal elevation and uncertainty maps

**Elevation product (page 6).** Intertidal height (m, MSL) and per-pixel uncertainty for the tutorial AOI.
```

*Figures are from the default tutorial coordinates; your maps will look different once you change the site.*

# Microsoft Planetary Computer

This tutorial uses [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com): a large, open catalogue of satellite data indexed via the **STAC** standard (SpatioTemporal Asset Catalog). Scenes sit as files in cloud storage, ready to be retrieved. You search the catalogue, pull the scenes you need to your own machine, and run the computation locally using the real DEA Intertidal algorithm.

For the core open collections — Landsat and Sentinel-2 — no account is needed. The function planetary_computer.sign() attaches short-lived access tokens to asset URLs so your machine can read them directly.

Because processing happens on your computer, you have full control over every step. The trade-off is that you carry the computational load: every scene is downloaded, so bandwidth and available memory set the practical ceiling for how large an area or how long a time series you can process in one go.

**Dask** helps manage this. The odc-stac loader returns lazy, Dask-backed arrays by default, streaming data through computation in chunks rather than loading everything into memory at once.

# Satellite techniques

Satellites measure the Earth in different ways. The two most relevant for coastal work are optical sensors and synthetic aperture radar.

**Optical sensors** work like a camera. They record sunlight reflected from the Earth's surface across a range of wavelengths — visible colours and, crucially for this method, near-infrared. Near-infrared is the key band: liquid water absorbs it almost completely, while dry sediment reflects it strongly. That contrast is what turns each satellite overpass into a wet-or-dry classification, and it is the foundation of the waterline method. The limitation is cloud cover — an optical sensor sees nothing through cloud, which is why we build composites from many scenes rather than relying on any one image.

**Synthetic Aperture Radar** (SAR) — such as Sentinel-1 — works entirely differently. It transmits its own microwave pulses and measures the return signal, making it independent of sunlight and cloud cover. It can image through overcast skies at night just as well as on a clear afternoon. In principle, this sounds ideal for tidal flats. In practice, radar backscatter is sensitive to surface roughness, moisture content, and the satellite's look-angle geometry, all of which vary across a tidal flat in ways that complicate a simple wet-or-dry interpretation. SAR can add value — particularly for detecting inundation in vegetated areas or under persistent cloud — but it requires substantially more preprocessing and different assumptions. This tutorial uses optical data; SAR remains an active research direction for extending the method.

## Open data versus commercial data

Choosing a sensor is also a financial and legal decision.

**Commercial providers** — such as Planet, Maxar, and Airbus — offer imagery at resolutions of 30 cm to 3 m, sometimes with daily revisit, and can be tasked to acquire images of a specific place at a specific time. The trade-off is cost, which is typically substantial (hundreds to thousands of euros per scene or per subscription), and licence restrictions that limit redistribution and publication of derived products. For exploratory research or teaching, commercial data is rarely practical.

**Free and open missions** are funded by public agencies and released without restriction. The two most important for intertidal science — Landsat and Sentinel-2 — are both in this category. They have been designed for long-term continuity, their archives are permanently accessible, and their calibration is well-documented. Every result in this tutorial can be reproduced by anyone, anywhere, at no cost.

## Landsat

Landsat is a joint NASA and USGS programme, operating continuously since 1972 and providing a consistent archive from Landsat 5 onward in the mid-1980s. It is the longest unbroken satellite record of the Earth's land surface ever assembled.

Its key specifications for this workflow:

- Resolution: ~30 metres per pixel (optical bands)
- Revisit: ~16 days per satellite; combined Landsat 8 and 9 give ~8 days
- Archive depth: back to 1984 with comparable sensors and calibration
- Data policy: free and open (USGS)

The deep archive is Landsat's defining advantage. A 30-metre pixel is coarse by modern standards, but for the waterline method, what matters is not resolution alone but the number of independent tide-level observations accumulated over time. With four decades of imagery, Landsat provides a stack of observations dense enough to reconstruct reliable elevation surfaces — and, critically, to compare two epochs separated by decades and ask how a flat has accreted or eroded.

When working across two time periods (as in a change-detection study), we use Landsat data for both the historical and modern epochs. Mixing sensors introduces resolution and spectral differences that can look like real morphological change. Consistency is worth more than sharpness.

## Sentinel-2

Sentinel-2 is part of the European Union's Copernicus programme, operated by ESA. The first satellite was launched in 2015; a second followed in 2017. A third (Sentinel-2C) joined the constellation in 2024, further improving revisit frequency.
Its key specifications:

- Resolution: 10 metres (red, green, blue, near-infrared) and 20 metres (red-edge, shortwave-infrared)
- Revisit: ~5 days at most latitudes with two satellites
- Archive depth: from 2015 onward
- Data policy: free and open (ESA/Copernicus)

The step from 30 to 10 metres is substantial for intertidal work: narrow channels, creek margins, and small-scale bedforms that are invisible in Landsat imagery become resolvable in Sentinel-2 imagery. The faster revisit time also means more observations per year, improving the statistical power of the elevation estimate within a shorter time window.

The limitation is simply that Sentinel-2 did not exist before 2015. For a present-day high-resolution map, this is no constraint at all. For a study that needs a historical baseline — asking what a flat looked like in 1990 — Sentinel-2 is not an option; Landsat is the only choice.

A processing note: Sentinel-2 changed its radiometric processing baseline in early 2022 (Baseline 04.00), introducing a +1000 DN offset in the reflectance values. Scenes from before and after that date must be harmonised before combining them into a composite.

# About this tutorial

The tutorial follows a deliberate sequence. Each one produces something the next page depends on: a working environment, a confirmed data connection, an understanding of the tidal signal at your site, a validated tide model, a visual sense of what the data looks like, and finally, the elevation map itself. Skipping pages is possible, but you will miss the diagnostic checks that tell you whether the final result can be trusted.

| Page | What you do |
|-----|---|
| **[Setup](01_setup.md)** | Install `uv`, clone the repo, create the Python environment *(instructions only — no code execution on the site)* |
| **[Connect](02_connect.ipynb)** | Test Planetary Computer (STAC search + signing) |
| **[Tides](03_tides.ipynb)** | Explore tidal range and satellite sampling at your site |
| **[Validation](04_validation.ipynb)** | Compare FES2022 against RWS gauge data (optional) |
| **[NDWI](05_ndwi.ipynb)** | Clear-sky RGB + NDWI at low and high tide — the logic behind height mapping |
| **[Elevation](06_elevation.ipynb)** | Full intertidal elevation map |

After the tutorial, or even before, read **[Applications & next steps](07_applications.md)** — what to do with the data,
time series, ecological monitoring. The idea is that your group will formulate its own research question to study over the next couple of days. 

Finished? Optionally remove the local install with **[Cleanup →](07_cleanup.md)**.

**Disclaimer & credits:** [Prof. Daphne van der Wal](mailto:Daphne.van.der.Wal@nioz.nl),
[Dr. Tim Grandjean](mailto:tim.grandjean@nioz.nl) — see **[Disclaimer →](08_disclaimer.md)**.

Ready? Start with **[1 · Setup →](01_setup.md)**.
