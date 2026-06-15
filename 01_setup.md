---
title: 1 · Setup — Environment & Installation
short_title: 1 · Setup
---

# Setting Up Your Environment

This first page takes you from a clean computer to a fully working environment with the
tutorial code and all dependencies installed. Work through it once, top to bottom. The
next page ([Initialising the data services](02_services.md)) then checks that the two data
backends — Google Earth Engine and Microsoft Planetary Computer — are reachable.

You will:

1. install **`uv`** (a fast, modern Python project manager),
2. **clone the tutorial repository** from GitHub,
3. install all dependencies into a locked, reproducible environment,
4. verify the install.

:::{note} Why `uv`?
`uv` replaces `pip`, `venv`, and `pyenv` with a single fast tool. It installs the correct
Python version for you and reproduces an *exact* environment from a lock file — which is
what makes scientific code reproducible. You do **not** need to install Python or GDAL
yourself; `uv` and the package wheels handle both.
:::

---

## Step 1 — Install `uv`

Run the one command for your operating system, then **close and reopen your terminal**.

::::{tab-set}
:::{tab-item} macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
:::
:::{tab-item} Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
:::
::::

Confirm it works:

```bash
uv --version
```

You should see a version number (e.g. `uv 0.11.x`). If you get "command not found", reopen
your terminal — on Windows, open a fresh PowerShell window.

---

## Step 2 — Get the tutorial code from GitHub

You need [`git`](https://git-scm.com/downloads) installed (check with `git --version`).
Then clone the repository and move into it:

```bash
git clone https://github.com/timgrandjean93/NCK-TidalFlat.git
cd NCK-TidalFlat
```

This downloads everything: both tutorial notebooks and the locked environment definitions.

:::{tip} No git? Download a ZIP instead
On the [repository page](https://github.com/timgrandjean93/NCK-TidalFlat), click the green
**Code** button → **Download ZIP**, unzip it, and `cd` into the unzipped folder. Cloning
with `git` is recommended because you can then pull updates with `git pull`.
:::

---

## Step 3 — Choose your route and install its dependencies

The tutorial offers two routes, each with its **own locked environment**. They are kept
separate on purpose: their dependency trees conflict (the Planetary Computer route pins an
older `rasterio` that the Earth Engine route does not want), so they must not share one
environment.

Pick the route you want now — you can set up the other one later by repeating this step in
its folder.

::::{tab-set}
:::{tab-item} Route 1 — Google Earth Engine
Cloud compute; needs a free Google account (set up on the next page).

```bash
cd gee
uv sync --frozen
```
:::
:::{tab-item} Route 2 — Planetary Computer + DEA
Local compute; **no account required**. Uses the real `intertidal.elevation()` algorithm.

```bash
cd pc
uv sync --frozen
```
:::
::::

What `uv sync --frozen` does, in one command:

1. installs **Python 3.12** if you don't already have it (uv manages Python itself);
2. creates a virtual environment in a local `.venv/` folder;
3. installs **every package at the exact version recorded in `uv.lock`** — the identical,
   tested set everyone else gets.

The `--frozen` flag means "use the lock file exactly, don't re-resolve". On a typical
connection this finishes in well under a minute.

:::{important} Folder layout in the repository
If your clone has the notebooks and the `gee/` and `pc/` environment folders at the top
level, the commands above are correct. If the notebooks sit at the repository root next to
a single environment, run `uv sync --frozen` from the root instead. The rule is simple:
run it in the folder that contains `pyproject.toml` and `uv.lock`.
:::

---

## Step 4 — Verify the install

Still inside your chosen route's folder, run the matching check.

::::{tab-set}
:::{tab-item} Route 1 — Earth Engine
```bash
uv run python -c "import ee, geemap, eo_tides, geopandas, rioxarray, xarray; print('Route 1 environment OK')"
```
:::
:::{tab-item} Route 2 — Planetary Computer
```bash
uv run python -c "from intertidal.elevation import elevation; import odc.stac, planetary_computer, eo_tides; print('Route 2 environment OK')"
```
:::
::::

If you see `... environment OK`, the environment is ready.

:::{dropdown} Troubleshooting
**`uv: command not found`** — reopen your terminal; on Windows use a fresh PowerShell.

**`uv` can't download Python (strict firewall/proxy)** — if you already have Python ≥ 3.12,
point uv at it: `uv sync --frozen --python $(which python3.12)` (macOS/Linux).

**Imports fail / "wrong kernel" later in Jupyter** — always start Jupyter from inside the
environment with `uv run jupyter lab`, not a system-wide Jupyter.

**Route 2: `intertidal.elevation` import error** — the locked environment pins
`eodatasets3==1.9.3` to avoid a `rasterio`/`datacube` conflict. If you changed the
dependencies, re-pin it and re-run `uv sync --frozen`.
:::

---

## Step 5 — Launch the notebook (when you're ready)

You don't need this yet — the next page runs in the same environment — but for reference,
this is how you open the actual tutorial notebook:

```bash
uv run jupyter lab
```

Your browser opens JupyterLab; double-click the notebook for your route.

---

## One more prerequisite: the FES2022 tide model

Both routes need the **FES2022** tide model on disk to convert acquisition times into water
levels. You can set this up now or when the notebook first asks for it.

Obtain it (free, with registration) from
[AVISO+](https://www.aviso.altimetry.fr/en/data/data-access/registration-form.html),
requesting the **FES (Finite Element Solution) tide** product, and arrange the constituent
files like this:

```
tide_models/
└── fes2022b/
    └── ocean_tide/
        ├── m2_fes2022.nc
        ├── s2_fes2022.nc
        └── ...   (~34 constituents)
```

This step is manual because AVISO requires an authenticated download. Each notebook has a
`TIDE_DIR` setting you point at this folder.

---

**Next:** [Initialising the data services →](02_services.md) — authenticate Earth Engine
(Route 1) or test the Planetary Computer connection (Route 2).
