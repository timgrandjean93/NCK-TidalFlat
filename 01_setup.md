---
title: 1 · Setup — Environment & Installation
short_title: 1 · Setup
execute:
  skip: true
---

# 1 · Setup — Environment & Installation

This page takes you from a clean computer to a fully working environment. The pages **2–7**
contain executable code; this page is instructions only (install `uv`, clone the repo,
install `.venv`).

The next page is **[2 · Connect — Planetary Computer](02_connect.ipynb)**.

You will:

1. install **`uv`** (a fast, modern Python project manager),
2. **clone the tutorial repository** from GitHub,
3. install all dependencies into the locked environment,
4. verify the install.

## Why `uv`?

Python has several tools for installing packages and managing environments, and they overlap in confusing ways. We chose uv for this tutorial because it does the most for the least effort — *but if you already work with another tool, you are welcome to keep using it*.

| Tool | Installs Python itself? | Manages environments? | Installs packages? | Lock file (exact reproducibility)? | Notes |
|---|---|---|---|---|---|
| **`uv`** | Yes | Yes | Yes | Yes (`uv.lock`) | One fast tool for everything; what this tutorial uses |
| pip + venv | No | Yes (`venv`) | Yes (`pip`) | Not by default | The classic built-in combination; you supply Python yourself |
| conda / Miniforge | Yes | Yes | Yes | Partial (`environment.yml`) | Strong for non-Python/compiled libraries; slower to resolve |
| Poetry | No | Yes | Yes | Yes (`poetry.lock`) | Project-focused; you supply Python yourself |

# Step 1 — Install `uv`

Run the one command for your operating system in a **terminal** (also called a command line or prompt).

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

# Step 2 — Open the working folder

The command `cd` ("change directory") moves you into a folder. If you are not sure where you
are: `pwd` (macOS/Linux) or `cd` on its own (Windows) prints your current location; `ls` or
`dir` lists what is in the folder.

# Step 3 — Get the material from GitHub

```bash
git --version
```

If you see a version number, clone the repository:

```bash
git clone https://github.com/timgrandjean93/NCK-TidalFlat.git
cd NCK-TidalFlat
```

:::{tip} No git? Download a ZIP instead
On the [repository page](https://github.com/timgrandjean93/NCK-TidalFlat), click **Code → Download ZIP**, unzip, and `cd` into the folder.
:::

# Step 4 — Install the environment

All notebooks and dependencies live in the **repository root**.

**Use Python 3.12 or 3.13 only.** Several packages (`llvmlite`, and on macOS also
`geomad`) need matching pre-built wheels or a one-time compile from source.

**Recommended (handles macOS compiler quirks automatically):**

```bash
chmod +x scripts/sync-env.sh   # once
./scripts/sync-env.sh
```

Or manually:

```bash
uv python install 3.12
uv sync --frozen
```

What this does:

1. installs **Python 3.12** via uv if needed (ignores Anaconda/system 3.11);
2. creates `.venv/` in the project folder;
3. installs every package at the exact version in `uv.lock`.

:::{warning} Do not use plain `pip install`
Install with **`uv sync --frozen`** (or `./scripts/sync-env.sh`) from the repo root.
Mixing conda/pip or installing without the lock file often triggers failed source builds.
:::

### If `geomad==1.0.0` fails to build (macOS)

`geomad` is a **Cython extension** pulled in by DEA/odc-algo. PyPI ships wheels for
**Linux and Windows only** — on **macOS it must compile locally** (~20 s with the
right compiler).

Typical error: `_Float16 is not supported on this target` or `command 'clang' failed`.

**Fix:**

1. Install Apple **Command Line Tools** (once): `xcode-select --install`
2. **Deactivate conda** (`conda deactivate`) — Anaconda's clang breaks this build
3. Reinstall with system clang:

   ```bash
   rm -rf .venv
   ./scripts/sync-env.sh
   ```

   Or explicitly:

   ```bash
   CC=/usr/bin/clang CXX=/usr/bin/clang++ uv sync --frozen --python 3.12
   ```

On **Windows/Linux**, `geomad` normally installs from a pre-built wheel (no compile).

:::{note} Harmless warning during macOS install
You may see: *"No GlobalOverrides context is active… SETUPTOOLS_SCM prefix"*.
That comes from **building geomad once** and does **not** affect the tutorial. `./scripts/sync-env.sh`
suppresses it; you can ignore it if you run `uv sync` manually.
:::

### If `llvmlite` still fails to build

1. Check Python inside the venv:

   ```bash
   uv run python -V
   ```

   Expected: `Python 3.12.x` or `Python 3.13.x`. If you see 3.11 or 3.14, remove the
   broken venv and reinstall:

   ```bash
   rm -rf .venv
   uv python install 3.12
   uv sync --frozen
   ```

2. On **Intel Macs** with Anaconda still on `PATH`, deactivate conda first
   (`conda deactivate`) or run sync with explicit Python:

   ```bash
   uv sync --frozen --python 3.12
   ```

3. Last resort on Intel Mac (compiler flags):

   ```bash
   CC=/usr/bin/clang CXX=/usr/bin/clang++ uv sync --frozen --python 3.12
   ```

# Step 5 — Verify the install

```bash
uv run python -c "from intertidal.elevation import elevation; import odc.stac, planetary_computer, eo_tides, geomad, llvmlite; print('Environment OK')"
```

# Step 6 — Launch Jupyter

```bash
uv run jupyter lab
```

Always start Jupyter from the **repository root** with `uv run jupyter lab`, not a system-wide install.

---

## Optional — build the website with executed notebooks

The tutorial site can **run notebooks at build time** and embed plots on your machine (not on
GitHub Pages). Use the helper scripts from the **repo root**:

**One-time setup:**

```bash
./scripts/sync-env.sh
uv run python -m ipykernel install --user --name nck --display-name "Python 3 (NCK)"
uv tool install jupyter-book
```

**Live preview with execution:**

```bash
./scripts/start-site-execute.sh
```

The script prints a **fixed Jupyter token** (default: `nck-local-execute`) and starts the
site at **http://localhost:3000**. You normally open **3000**, not the Jupyter port (8888).

**Static build with execution:**

```bash
./scripts/build-site-execute.sh
```

---

# Step 7 — The tide model

The tutorial needs the **FES2022** tide model on disk. Arrange the constituent files like this:

```
tide_models/
└── fes2022b/
    └── ocean_tide_20241025/
        ├── m2_fes2022.nc
        ├── s2_fes2022.nc
        └── ...   (~34 constituents)
```

Point each notebook's `TIDE_DIR` at the folder containing `fes2022b/`.

:::{note} Taking this as a course?
You can get the FES2022 files directly from **Tim Grandjean** — no AVISO registration needed.
:::

---

**Next:** [2 · Connect — Planetary Computer →](02_connect.ipynb)
