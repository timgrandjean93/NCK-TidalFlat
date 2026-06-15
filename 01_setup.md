---
title: 1 · Setup — Environment & Installation
short_title: 1 · Setup
execute:
  skip: true
---

This page takes you from a clean computer to a working environment. It contains
instructions only — no code is executed here. Pages 2–6 contain the actual analysis.

# Step 1 — Install `uv`

`uv` is a Python project manager that installs the correct Python version for you,
creates an isolated environment, and ensures everyone working with this tutorial gets
identical package versions. You do not need to install Python first.

Open a terminal and run the command for your system:

::::{tab-set}
:::{tab-item} macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Close and reopen your terminal, then confirm it worked:
```bash
uv --version
```
:::
:::{tab-item} Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Open a new PowerShell window, then confirm:
```powershell
uv --version
```
:::
::::

> **New to terminals?** A terminal is a window where you type commands. On macOS open
> *Terminal* (`Cmd + Space` → "Terminal"). On Windows open *PowerShell*
> (Start → "PowerShell"). The command `pwd` prints your current location; `ls`
> (macOS/Linux) or `dir` (Windows) lists what is in the current folder.

---

# Step 2 — Get the tutorial code

Check that `git` is available:

```bash
git --version
```

Then clone the repository and move into it:

```bash
git clone https://github.com/timgrandjean93/NCK-TidalFlat.git
cd NCK-TidalFlat
```

:::{tip} No git?
On the [repository page](https://github.com/timgrandjean93/NCK-TidalFlat), click
**Code → Download ZIP**, unzip the file, and `cd` into the resulting folder.
Cloning with `git` is preferred because you can pull updates later with `git pull`.
:::

---

# Step 3 — Install the environment

From inside the `NCK-TidalFlat` folder, run:

```bash
./scripts/sync-env.sh
```

This single script does everything: it installs Python 3.12, creates a `.venv/` folder,
and installs all packages at the exact versions recorded in `uv.lock`. It also handles
the macOS-specific compiler requirements automatically.

On **Windows**, run the equivalent directly:

```powershell
uv python install 3.12
uv sync --frozen
```

The first run takes a few minutes. Subsequent runs are instant.

---

# Step 4 — Verify the install

```bash
uv run python -c "from intertidal.elevation import elevation; import odc.stac, planetary_computer, eo_tides; print('Environment OK')"
```

If you see `Environment OK`, everything is in place.

---

# Step 5 — Get the FES2022 tide model

The tutorial needs the FES2022 tide model files on disk from page 3 onward.

**Where to get the files**

| Route | Who | Notes |
|---|---|---|
| **Course / NCK participants** | [Tim Grandjean](mailto:tim.grandjean@nioz.nl) | Pre-packaged `tide_models/` folder; no AVISO registration |
| **Self-service** | [AVISO+ / CNES](https://www.aviso.altimetry.fr/en/data/products/auxiliary-products/global-tide-fes.html) | Free registration; download **FES2022b** ocean tide constituents (~1 GB) |

Arrange them like this:

```
tide_models/
└── fes2022b/
    └── ocean_tide_20241025/
        ├── m2_fes2022.nc
        ├── s2_fes2022.nc
        └── ...
```

Set `TIDE_DIR` in each notebook to the folder containing `fes2022b/` (default:
`./tide_models`).

---

# Step 6 — Launch Jupyter

All analysis pages in this tutorial (**Connect** through **Elevation**, pages 2–6) are
**Jupyter notebooks** (`.ipynb`). Open them in Jupyter and run the cells from top to
bottom — each notebook is self-contained and executable once this setup is complete.

```bash
uv run jupyter lab
```

JupyterLab opens in your browser. Use the file browser on the left to open
`02_connect.ipynb`, then continue in order through `06_elevation.ipynb`. Run a cell
with **Shift + Enter** (or the ▶ Run button).

Prefer the classic interface? That works too:

```bash
uv run jupyter notebook
```

Always start Jupyter from the **repository root** with `uv run` so the `nck` environment
and packages are used — not a system-wide Python install.

:::{tip} Reading vs running
You can also read this site in the browser (`jupyter book start`), but to **execute** the
analysis yourself, use Jupyter Lab or Notebook as above.
:::

---

# Troubleshooting

:::{dropdown} Troubleshooting — installation problems

**`uv: command not found`**
Close and reopen your terminal. On Windows, open a new PowerShell window.

---

**macOS: `omp.h file not found` or `geomad` build failure**
OpenMP is missing. Install Homebrew and then `libomp`:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install libomp
rm -rf .venv && ./scripts/sync-env.sh
```

---

**macOS: `_Float16 is not supported on this target`**
Anaconda's compiler is interfering. Run `conda deactivate` first, then retry:
```bash
rm -rf .venv && ./scripts/sync-env.sh
```

---

**`llvmlite` build failure**
Check your Python version:
```bash
uv run python -V
```
Expected: `Python 3.12.x`. If you see 3.11 or 3.14, reinstall:
```bash
rm -rf .venv && uv python install 3.12 && uv sync --frozen
```

---

**Wrong kernel in Jupyter**
Always start Jupyter with `uv run jupyter lab` from the repo root,
not a system-wide Jupyter installation.

:::

---

**Next:** [2 · Connect →](02_connect.ipynb)