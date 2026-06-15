---
title: 2 · Connecting to the Data Services
short_title: 2 · Data Services
---

# Initialising Earth Engine / Testing Planetary Computer

With your environment installed ([previous page](01_setup.md)), this page confirms that the
data backend for your route is reachable **before** you start the full analysis. Each route
talks to a different service:

- **Route 1 (Earth Engine)** needs a one-time account authentication.
- **Route 2 (Planetary Computer)** needs no account — we just confirm the catalogue answers.

Run the snippet for your route. You can paste it into a Jupyter cell (`uv run jupyter lab`)
or run it directly from the terminal with `uv run python`.

---

## Route 1 — Initialising Google Earth Engine

Earth Engine is free for research and education but requires a **one-time registration**
tied to a Google Cloud project.

### Step 1 — Register (once per Google account)

1. Go to [earthengine.google.com](https://earthengine.google.com/) and register.
2. Create or select a **Cloud Project** — a free *non-commercial* project is sufficient.
3. Note the **project ID** (it looks like `ee-yourname`). You supply it below.

### Step 2 — Authenticate and initialise

Run this in your `gee` environment. The first run opens a browser window where you grant
access and paste back a token; the credentials are then stored locally, so later sessions
skip this.

```python
import ee

EE_PROJECT = "ee-replace-me"   # <-- your Cloud Project ID

try:
    ee.Initialize(project=EE_PROJECT)
    print("Earth Engine initialised (existing credentials found).")
except Exception:
    ee.Authenticate()                  # interactive, one time per machine
    ee.Initialize(project=EE_PROJECT)
    print("Authentication successful; Earth Engine initialised.")
```

### Step 3 — Confirm the connection

```python
import ee
count = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").limit(5).size().getInfo()
print("Earth Engine connection OK. Probe collection size:", count)
```

If this prints a number, Route 1 is ready and you can open
`intertidal_elevation_GEE_tutorial.ipynb`.

:::{dropdown} Earth Engine troubleshooting
**`ee.Initialize` fails with a project error** — the project ID is wrong, or Earth Engine
isn't enabled for it. Re-check the ID at
[code.earthengine.google.com](https://code.earthengine.google.com) (top-left project
selector).

**The browser step won't complete on a headless/remote machine** — run
`earthengine authenticate --quiet` and follow the URL-based flow, or authenticate once on a
machine with a browser and copy the credentials file.

**"Not signed up"** — your Google account hasn't been registered for Earth Engine yet
(Step 1).
:::

---

## Route 2 — Testing the Planetary Computer connection

The Microsoft Planetary Computer STAC catalogue and its open collections (Landsat,
Sentinel-2) are **anonymously accessible** — no account, no key. The function
`planetary_computer.sign()` attaches short-lived access tokens to asset URLs so they can be
read. A free subscription key only raises rate limits and unlocks a few premium datasets
(e.g. Sentinel-1 RTC); it is **not** needed for this tutorial.

### Step 1 — Confirm the catalogue answers a search

Run this in your `pc` environment:

```python
import pystac_client
import planetary_computer

PC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
catalog = pystac_client.Client.open(PC_URL, modifier=planetary_computer.sign_inplace)

# A tiny search over a small area / short window just to prove connectivity.
search = catalog.search(
    collections=["landsat-c2-l2"],
    bbox=(3.96, 51.55, 4.10, 51.62),     # example: part of the Oosterschelde, NL
    datetime="2023-01-01/2023-03-31",
    query={"eo:cloud_cover": {"lt": 80}},
)
items = search.item_collection()
print(f"Planetary Computer connection OK. Found {len(items)} Landsat scenes in the test window.")
```

If this prints a scene count (any number ≥ 0 without an error), the connection works.

### Step 2 — Confirm an asset can be signed and read

This checks that signing works — the step that replaces an account:

```python
import planetary_computer

if len(items) > 0:
    item = items[0]
    signed = planetary_computer.sign(item)
    # A signed asset href carries a temporary access token:
    href = signed.assets["red"].href
    print("Signing OK — assets are readable. Example signed href starts with:")
    print(href.split("?")[0], "(+ access token)")
else:
    print("No scenes in the test window; widen bbox or dates and retry.")
```

If signing succeeds, Route 2 is ready and you can open
`intertidal_elevation_PC_tutorial.ipynb`.

:::{dropdown} Planetary Computer troubleshooting
**Search returns 0 scenes** — widen the `bbox` or `datetime`, or raise the cloud-cover
limit. Zero results is a query issue, not a connection failure.

**Network/TLS errors** — confirm you can reach
`https://planetarycomputer.microsoft.com`; corporate proxies sometimes block it.

**You want higher rate limits** — request a free key at the
[Planetary Computer](https://planetarycomputer.microsoft.com/) site and set it via the
`planetary-computer` library's configuration. Not required for this tutorial.
:::

---

## You're connected — what's next

Once your route's check passes, open its notebook and work through the full analysis:

::::{tab-set}
:::{tab-item} Route 1 — Earth Engine
```bash
uv run jupyter lab
# open intertidal_elevation_GEE_tutorial.ipynb
```
:::
:::{tab-item} Route 2 — Planetary Computer
```bash
uv run jupyter lab
# open intertidal_elevation_PC_tutorial.ipynb
```
:::
::::

The notebooks pick up exactly where this page leaves off: defining a study area, loading
imagery, modelling tides with FES2022, and producing the intertidal elevation surface.
