---
title: Mapping Intertidal Elevation from Open Satellite Data
---

# Background

Tidal flats are surveyed, but rarely often enough. The Westerschelde is mapped yearly; the Waddenzee only about once every five years; many estuaries far less than that. Each survey — by survey vessel or aircraft — is expensive, logistically awkward, and a single snapshot of a surface that can shift by metres within a season. The result is a record full of gaps, in a landscape that never stops moving.

That mismatch is the opening for an alternative. Rather than visiting the flats, we let the satellites that already pass overhead, hundreds of times per decade, do the measuring — turning an irregular, costly survey into a continuous, free, and globally consistent one.

### The core idea

A satellite images each coastal pixel across many tide levels over the years. Sort those observations by tide height and a pixel flips from dry to wet at one particular level — and that crossover height is, to first order, the elevation of the sediment surface there. Do it for every pixel and you have an intertidal Digital Elevation Model. Everything that follows is a careful execution of that single principle.

### Why it takes care

The idea is simple; making it trustworthy is the work. Four things stand in the way, and the tutorial handles each:
Globally, we always miss information about the measured tidal height measure the tide directly, so we model it. Which also means we can hindcast back to the 1980s, enabling decade-scale comparison. We turn "wet or dry" into a number with the NDWI water index from each scene's green and near-infrared bands. We remove cloud, shadow, and noise per scene, and accumulate many clear views over a multi-year window rather than trusting any one image. And we watch for tidal sampling bias: a pixel's elevation can only be found if it was observed both below and above its crossover height — if every clear image caught high water, the low flats are never seen dry.

# The data platform — Microsoft Planetary Computer

This tutorial uses **Microsoft Planetary Computer**: a vast, open catalogue of satellite data — indexed using the **STAC** standard (SpatioTemporal Asset Catalog) — where scenes sit as files in the cloud, ready to be retrieved. You search the catalogue for the scenes you need, pull them to your own machine, and run the computation locally with the real **DEA Intertidal** `intertidal.elevation()` algorithm.

For the core open collections, including Landsat and Sentinel-2, **no account is needed** — access is anonymous. The function `planetary_computer.sign()` attaches short-lived access tokens to asset URLs so your machine can read the files.

Because processing happens on your computer, you are in full control: you can run any algorithm you like. The cost of that freedom is that you carry the load yourself — every scene is downloaded, so bandwidth and memory set the practical ceiling.

**Dask** helps here. The `odc-stac` loader returns lazy, Dask-backed arrays by default, so data is streamed through computation in manageable chunks rather than loaded entirely into RAM at once.

# Optical Satellite Data

The tutorial relies on optical satellite imagery — sensors that record sunlight reflected off the Earth's surface across visible and near-infrared wavelengths. That near-infrared sensitivity lets us tell water from land: water absorbs it strongly, dry sediment does not. The one limitation is clouds, which is why we work with long stacks of images and discard cloud-covered pixels.

The two missions we use, **Landsat** and **Sentinel-2**, are both freely and openly available.

*A brief note on radar (Sentinel-1): it sees through clouds, but measures the surface differently and is not part of this optical workflow.*

## Landsat

Landsat is the longest continuous record of the Earth's land surface — imaging since 1972, with comparable data from Landsat 5 onward in the mid-1980s. Its imagery comes at roughly **30-metre** resolution, with revisit about every sixteen days per satellite. For the waterline method, what matters is the deep archive: many observations over years, each at a slightly different tide level.

## Sentinel-2

Sentinel-2 (Copernicus, from 2015) offers **10-metre** resolution in key bands and revisit every ~5 days (two satellites). Finer detail and denser tidal sampling within any given period — but no history before 2015.

# About this tutorial

Follow these seven pages in order:

| Page | What you do |
|---|---|
| **[1 · Setup](01_setup.md)** | Install `uv`, clone the repo, create the Python environment *(instructions only — no code execution on the site)* |
| **[2 · Connect](02_connect.ipynb)** | Test Planetary Computer (STAC search + signing) |
| **[3 · Tides](03_tides.ipynb)** | Explore tidal range and satellite sampling at your site |
| **[4 · Validation](04_validation.ipynb)** | Compare FES2022 against RWS gauge data (optional) |
| **[5 · Composites](05_composites.ipynb)** | Load Sentinel-2 pixels — low- and high-tide RGB composites |
| **[6 · NDWI](06_ndwi.ipynb)** | How NDWI separates wet from dry — the logic behind height mapping |
| **[7 · Elevation](07_elevation.ipynb)** | Full intertidal elevation map with `intertidal.elevation()` |

*For FES2022 tide files during the course, ask Tim.*

Ready? Start with **[1 · Setup →](01_setup.md)**.
