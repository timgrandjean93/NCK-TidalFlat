# Mapping Intertidal Elevation — Tutorial Site

A graduate-level, reproducible tutorial for mapping intertidal elevation from open
satellite imagery (Landsat) and the FES2022 tide model, with two routes:

- **Route 1 — Google Earth Engine** (`gee/`): cloud compute, needs a Google account.
- **Route 2 — Planetary Computer + DEA Intertidal** (`pc/`): local compute, no account,
  uses the real `intertidal.elevation()` algorithm.

This repository is also a **website**: it is built with [Jupyter Book 2](https://jupyterbook.org)
(the MyST Document Engine) and deployed automatically to GitHub Pages.

## Repository layout

```
.
├── myst.yml                     # site config + table of contents
├── index.md                     # landing page
├── gee/
│   ├── intertidal_elevation_GEE_tutorial.ipynb
│   ├── pyproject.toml + uv.lock         # uv environment for Route 1
│   └── environment.yml + requirements.txt   # conda fallback
├── pc/
│   ├── intertidal_elevation_PC_tutorial.ipynb
│   └── pyproject.toml + uv.lock         # uv environment for Route 2
└── .github/workflows/deploy.yml # builds + publishes the site on every push
```

---

## Publishing the site (one-time GitHub setup)

You need a GitHub account and an empty repository. Then:

### 1. Put this folder under version control and push it

From inside this folder:

```bash
git init
git add .
git commit -m "Intertidal elevation tutorial: initial site"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

### 2. Tell the config where the repo lives

Edit `myst.yml` and replace the `View on GitHub` URL under `site.actions` with your
repository URL. Commit and push that change.

### 3. Turn on GitHub Pages (once)

On GitHub: **Settings -> Pages -> Build and deployment -> Source: GitHub Actions**.

That's it. The included workflow (`.github/workflows/deploy.yml`) runs on every push to
`main`, builds the site, and publishes it. After the first run finishes (watch the
**Actions** tab), your site is live at:

```
https://YOUR-USERNAME.github.io/YOUR-REPO/
```

### Updating the site

Just edit content and push — the site rebuilds automatically:

```bash
git add .
git commit -m "Update tutorial"
git push
```

---

## Important: the notebooks are NOT executed by the build

The build publishes the notebooks **exactly as committed** (`myst.yml` sets
`jupyter: false`). This is deliberate: the notebooks need interactive Earth Engine
authentication, a registered AVISO download, and local tide files — none of which can run
on a GitHub build server.

**Therefore, commit the notebooks with the cell output you want visitors to see.** Two
sensible options:

- **Run them locally first**, then commit so the rendered figures/maps appear on the site.
- **Or clear all output** (`Kernel -> Restart & Clear Output` in Jupyter) and commit, if
  you prefer to show code only and have readers run it themselves.

Either is fine — just decide which, because the website mirrors whatever is in the `.ipynb`.

---

## Previewing the site locally (optional)

Install Jupyter Book and run a live preview:

```bash
pip install "jupyter-book==2.1.5"
jupyter book start          # live preview at http://localhost:3000
# or a one-off static build:
jupyter book build --html   # output in _build/html/
```

---

## Running the tutorials

See the landing page (`index.md`) for full setup, or in brief, from either route's folder:

```bash
# install uv once (see index.md), then:
cd gee        # or: cd pc
uv sync --frozen
uv run jupyter lab
```

Both routes also need the FES2022 tide model on disk — see the note on the landing page for
the AVISO download and the expected folder layout. Tide files and other large/local data are
intentionally git-ignored (see `.gitignore`); do not commit them.
