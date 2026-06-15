"""
cache_utils.py
--------------
Shared caching helpers for the NCK-TidalFlat tutorial notebooks.

All three computationally expensive steps — (1) running FES2022 for a continuous
tide series, (2) querying Planetary Computer and tagging scenes with tide heights,
and (3) downloading RWS gauge data via ddlpy — are wrapped in functions that check
for an existing Parquet file before running. If the file exists it is loaded directly;
if not, the computation runs and the result is saved.

Cache files live in a subfolder called 'cache/' next to the notebooks, organised as:

    cache/
        tides_<site>_<start>_<end>.parquet      continuous 30-min FES2022 series
        scenes_<site>_<start>_<end>.parquet     satellite scenes + tagged tide height
        gauge_<station>_<start>_<end>.parquet   RWS DDL gauge measurements

All Parquet files store timestamps as UTC-aware, so they round-trip correctly
through pandas without losing timezone information.

Usage
-----
from cache_utils import load_or_compute_tides, load_or_compute_scenes, load_or_compute_gauge
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CACHE_DIR = Path("cache")


def _slug(text: str) -> str:
    """Make a safe filename fragment from an arbitrary string."""
    return re.sub(r"[^A-Za-z0-9_-]", "_", str(text)).strip("_")


def _cache_path(prefix: str, site: str, start: str, end: str, extra: str = "") -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    parts = [prefix, _slug(site)]
    if extra:
        parts.append(_slug(extra))
    parts.extend([_slug(start), _slug(end)])
    return CACHE_DIR / ("_".join(parts) + ".parquet")


def _sensor_slug(sensors: list[str]) -> str:
    """Short cache-key fragment for a sensor selection, e.g. 's2-l8-l9'."""
    mapping = {"Sentinel-2": "s2", "Landsat 8": "l8", "Landsat 9": "l9"}
    return "-".join(mapping[s] for s in sensors if s in mapping) or "none"


def _utc_datetime_ns(values) -> pd.DatetimeIndex:
    """Coerce datetime-like values to ``datetime64[ns, UTC]`` for safe alignment."""
    return pd.to_datetime(values, utc=True).astype("datetime64[ns, UTC]")


def _save(df: pd.DataFrame, path: Path) -> None:
    """Save a DataFrame to Parquet, converting tz-aware index to UTC."""
    out = df.copy()
    if isinstance(out.index, pd.DatetimeIndex):
        out.index = _utc_datetime_ns(out.index)
    out.to_parquet(path)
    print(f"  Cached → {path}  ({len(out):,} rows)")


def _load(path: Path) -> pd.DataFrame:
    """Load a Parquet file and restore a UTC DatetimeIndex."""
    df = pd.read_parquet(path)
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = _utc_datetime_ns(df.index)
    print(f"  Loaded from cache ← {path}  ({len(df):,} rows)")
    return df


def _tag_scenes_with_tides(
    scene_df: pd.DataFrame,
    lon: float,
    lat: float,
    start: str,
    end: str,
    site_name: str,
    tide_model: str,
    tide_dir: str,
) -> pd.DataFrame:
    """Attach tide_height to satellite scenes using the cached FES2022 series.

    Scene times from STAC are timezone-aware with sub-second precision; eo-tides
    returns timezone-naive nanosecond timestamps. Exact index lookup therefore
    fails — we match with merge_asof (nearest 30-minute model timestep).
    """
    if scene_df.empty:
        return scene_df

    scene_df = scene_df.copy()
    scene_df["time"] = _utc_datetime_ns(scene_df["time"])

    tide_series = load_or_compute_tides(
        lon=lon,
        lat=lat,
        start=start,
        end=end,
        site_name=site_name,
        tide_model=tide_model,
        tide_dir=tide_dir,
        overwrite=False,
    )
    tide_ref = pd.DataFrame(
        {
            "time": _utc_datetime_ns(tide_series.index),
            "tide_height": tide_series.values,
        }
    ).sort_values("time")

    tagged = pd.merge_asof(
        scene_df.sort_values("time"),
        tide_ref,
        on="time",
        direction="nearest",
        tolerance=pd.Timedelta("30min"),
    )
    n_ok = int(tagged["tide_height"].notna().sum())
    print(f"  Tagged {n_ok}/{len(tagged)} scenes with tide heights (±30 min)")
    return tagged.sort_values("time").reset_index(drop=True)


# ---------------------------------------------------------------------------
# 1. Continuous FES2022 tide series
# ---------------------------------------------------------------------------

def load_or_compute_tides(
    lon: float,
    lat: float,
    start: str,
    end: str,
    site_name: str,
    tide_model: str,
    tide_dir: str,
    freq: str = "30min",
    overwrite: bool = False,
) -> pd.Series:
    """Return a continuous tide-height Series (m, MSL) at 30-min intervals.

    Loads from cache if available; runs FES2022 via eo-tides otherwise.

    Parameters
    ----------
    lon, lat    : WGS84 coordinates of the evaluation point.
    start, end  : ISO date strings ('YYYY-MM-DD').
    site_name   : Used in the cache filename.
    tide_model  : e.g. 'FES2022'.
    tide_dir    : Directory containing the tide model constituent files.
    freq        : Pandas frequency string for the time axis (default '30min').
    overwrite   : If True, ignore existing cache and recompute.

    Returns
    -------
    pd.Series with DatetimeIndex (UTC), values in metres (MSL).
    """
    path = _cache_path("tides", site_name, start, end)

    if path.exists() and not overwrite:
        df = _load(path)
        return df["tide_height"]

    print(f"Computing FES2022 at ({lat:.4f} N, {lon:.4f} E) "
          f"for {start} to {end} at {freq} intervals ...")

    from eo_tides.model import model_tides

    times = pd.date_range(start, end, freq=freq, tz="UTC")
    raw = model_tides(
        x=[lon], y=[lat],
        time=times,
        model=tide_model,
        directory=tide_dir,
    )
    heights = (
        raw.reset_index()
        .groupby("time")["tide_height"]
        .mean()
        .rename("tide_height")
    )
    heights.index = _utc_datetime_ns(heights.index)
    _save(heights.to_frame(), path)
    return heights


# ---------------------------------------------------------------------------
# 2. Satellite scenes + tide-tagged heights
# ---------------------------------------------------------------------------

def load_or_compute_scenes(
    lon: float,
    lat: float,
    start: str,
    end: str,
    site_name: str,
    tide_model: str,
    tide_dir: str,
    max_cloud: int = 80,
    delta: float = 0.05,
    overwrite: bool = False,
    sensors: list[str] | None = None,
) -> pd.DataFrame:
    """Return a DataFrame of satellite scenes with tagged tide heights.

    Queries Planetary Computer for Sentinel-2, Landsat 8 and/or Landsat 9 scenes
    over the given bounding box and time window, then tags each with the FES2022
    tide height at the acquisition time.

    Loads from cache if available.

    Parameters
    ----------
    lon, lat    : WGS84 coordinates of the site centre.
    start, end  : ISO date strings.
    site_name   : Used in the cache filename.
    tide_model  : e.g. 'FES2022'.
    tide_dir    : Directory containing the tide model constituent files.
    max_cloud   : Scene-level cloud-cover ceiling (%, default 80).
    delta       : Half-width of the bounding box in degrees (default 0.05°).
    overwrite   : If True, ignore existing cache and recompute.
    sensors     : Which sensors to query. Default: all three.
                  Options: ``"Sentinel-2"``, ``"Landsat 8"``, ``"Landsat 9"``.

    Returns
    -------
    pd.DataFrame with columns: sensor, time (UTC), cloud_cover, tide_height, item_id.
    """
    all_sensors = ("Sentinel-2", "Landsat 8", "Landsat 9")
    if sensors is None:
        sensors = list(all_sensors)
    else:
        sensors = [s for s in sensors if s in all_sensors]
    if not sensors:
        raise ValueError(f"sensors must include at least one of {all_sensors}")

    path = _cache_path("scenes", site_name, start, end, extra=_sensor_slug(sensors))

    if path.exists() and not overwrite:
        return _load(path).reset_index()

    import pystac_client
    import planetary_computer

    bbox = (lon - delta, lat - delta, lon + delta, lat + delta)
    PC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
    catalog = pystac_client.Client.open(PC_URL, modifier=planetary_computer.sign_inplace)

    SENSORS = {
        "Sentinel-2": {
            "collections": ["sentinel-2-l2a"],
            "query": {"eo:cloud_cover": {"lt": max_cloud}},
        },
        "Landsat 8": {
            "collections": ["landsat-c2-l2"],
            "query": {"platform": {"in": ["landsat-8"]},
                      "eo:cloud_cover": {"lt": max_cloud}},
        },
        "Landsat 9": {
            "collections": ["landsat-c2-l2"],
            "query": {"platform": {"in": ["landsat-9"]},
                      "eo:cloud_cover": {"lt": max_cloud}},
        },
    }

    rows = []
    for sensor in sensors:
        cfg = SENSORS[sensor]
        print(f"  Querying PC for {sensor} ...")
        search = catalog.search(
            collections=cfg["collections"],
            bbox=bbox,
            datetime=f"{start}/{end}",
            query=cfg["query"],
        )
        items = list(search.items())
        if not items:
            continue

        times = pd.to_datetime([i.datetime for i in items], utc=True)
        cloud = [i.properties.get("eo:cloud_cover", np.nan) for i in items]

        for item, t, c in zip(items, times, cloud):
            rows.append({
                "sensor":      sensor,
                "time":        t,
                "cloud_cover": c,
                "item_id":     item.id,
            })

    df = _tag_scenes_with_tides(
        pd.DataFrame(rows),
        lon=lon,
        lat=lat,
        start=start,
        end=end,
        site_name=site_name,
        tide_model=tide_model,
        tide_dir=tide_dir,
    )

    _save(df.set_index("time"), path)
    return df


_SENSOR_STAC_COLLECTION: dict[str, str] = {
    "Sentinel-2": "sentinel-2-l2a",
    "Landsat 8": "landsat-c2-l2",
    "Landsat 9": "landsat-c2-l2",
}


def _fetch_stac_items_one_collection(
    catalog,
    selected_scenes: pd.DataFrame,
    bbox: tuple[float, float, float, float],
    collection: str,
) -> list:
    """Fetch STAC items for one collection via item_id or nearest-time match."""
    if selected_scenes.empty:
        return []

    if "item_id" in selected_scenes.columns:
        ids = selected_scenes["item_id"].dropna().unique().tolist()
        if ids:
            items = list(catalog.search(collections=[collection], ids=ids).items())
            if items:
                by_id = {it.id: it for it in items}
                ordered = [by_id[i] for i in ids if i in by_id]
                if ordered:
                    return ordered

    scenes = selected_scenes.copy()
    scenes["time"] = _utc_datetime_ns(scenes["time"])
    t_min = scenes["time"].min().strftime("%Y-%m-%d")
    t_max = scenes["time"].max().strftime("%Y-%m-%d")

    search = catalog.search(
        collections=[collection],
        bbox=bbox,
        datetime=f"{t_min}/{t_max}",
        query={"eo:cloud_cover": {"lt": 100}},
    )

    stac_rows = []
    for item in search.items():
        stac_rows.append({
            "time": _utc_datetime_ns([item.datetime])[0],
            "item": item,
        })
    if not stac_rows:
        return []

    stac_df = pd.DataFrame(stac_rows).sort_values("time")
    scenes_sorted = scenes[["time"]].sort_values("time")
    matched = pd.merge_asof(
        scenes_sorted,
        stac_df,
        on="time",
        direction="nearest",
        tolerance=pd.Timedelta("2min"),
    )
    items = [
        row.item for row in matched.itertuples()
        if getattr(row, "item", None) is not None and not pd.isna(getattr(row, "item", None))
    ]
    seen: set[str] = set()
    unique = []
    for it in items:
        if it.id not in seen:
            seen.add(it.id)
            unique.append(it)
    return unique


def fetch_stac_items_for_scenes(
    catalog,
    selected_scenes: pd.DataFrame,
    bbox: tuple[float, float, float, float],
    collection: str | None = None,
) -> list:
    """Return Planetary Computer STAC items for tagged scene rows.

    Prefer direct lookup by ``item_id`` (stored since cache_utils update). Older
    caches without ``item_id`` fall back to nearest-time matching (±2 min) over a
    bbox/date search — no ``platform`` filter (PC uses ``Sentinel-2A`` casing).

    When ``collection`` is None and a ``sensor`` column is present, items are
    fetched per sensor (Sentinel-2, Landsat 8/9).
    """
    if selected_scenes.empty:
        return []

    if collection is not None:
        return _fetch_stac_items_one_collection(catalog, selected_scenes, bbox, collection)

    if "sensor" in selected_scenes.columns:
        items: list = []
        for sensor, group in selected_scenes.groupby("sensor"):
            coll = _SENSOR_STAC_COLLECTION.get(sensor)
            if not coll:
                continue
            items.extend(_fetch_stac_items_one_collection(catalog, group, bbox, coll))
        return items

    return _fetch_stac_items_one_collection(
        catalog, selected_scenes, bbox, "sentinel-2-l2a"
    )


# ---------------------------------------------------------------------------
# 3. RWS gauge data via ddlpy
# ---------------------------------------------------------------------------

# Legacy RWS codes → current ddlpy location index (WaterWebservices / ddapi20).
_GAUGE_STATION_ALIASES: dict[str, str] = {
    "HOEKVHLD": "hoekvanholland",
    "DENHDR": "denhelder.marsdiep",
    "HARLGN": "harlingen.waddenzee",
    "DELFZL": "delfzijl",
    "VLISSGN": "vlissingen",
    "YERSEKE": "yerseke",
    "ROOMPOT": "oosterschelde.roompotsluis.buiten",
}


def _resolve_gauge_station(wathte: pd.DataFrame, station_code: str) -> pd.DataFrame:
    """Find WATHTE/NAP rows for a station code, name, or ddlpy location index."""
    key = station_code.strip()
    alias = _GAUGE_STATION_ALIASES.get(key.upper())
    if alias:
        key = alias

    station = wathte[wathte.index == key]
    if station.empty:
        station = wathte[wathte.index.str.contains(key, case=False, na=False)]
    if station.empty and "Naam" in wathte.columns:
        station = wathte[wathte["Naam"].astype(str).str.contains(key, case=False, na=False)]
    if station.empty:
        sample = sorted(wathte.index.unique())[:15]
        raise ValueError(
            f"Station {station_code!r} not found in ddlpy catalogue. "
            f"Use a ddlpy index (e.g. 'denhelder.marsdiep') or legacy code 'DENHDR'. "
            f"Examples: {sample}"
        )

    if "Hoedanigheid.Code" in station.columns and (station["Hoedanigheid.Code"] == "NAP").any():
        station = station[station["Hoedanigheid.Code"] == "NAP"]

    if len(station) > 1 and key in station.index:
        station = station.loc[[key]]

    return station


def _gauge_value_column(raw: pd.DataFrame) -> str:
    for col in ("Meetwaarde.Waarde_Numeriek", "Waarde_Numeriek"):
        if col in raw.columns:
            return col
    raise KeyError(
        "Unexpected ddlpy response — no numeric water-level column. "
        f"Columns: {list(raw.columns)}"
    )


def list_gauge_stations(name_filter: str = "", limit: int = 20) -> pd.DataFrame:
    """List WATHTE/NAP tide-gauge locations (notebook helper)."""
    import ddlpy

    locs = ddlpy.locations()
    wathte = locs[locs["Grootheid.Code"] == "WATHTE"]
    if "Hoedanigheid.Code" in wathte.columns:
        wathte = wathte[wathte["Hoedanigheid.Code"] == "NAP"]
    if name_filter:
        mask = (
            wathte.index.str.contains(name_filter, case=False, na=False)
            | wathte["Naam"].astype(str).str.contains(name_filter, case=False, na=False)
        )
        wathte = wathte[mask]
    cols = [c for c in ["Naam", "Lat", "Lon", "Groepering.Code"] if c in wathte.columns]
    return wathte[cols].reset_index().drop_duplicates(subset=["Code"]).head(limit)


def _dataframe_with_time_column(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with ``time`` as a UTC datetime column (not the index)."""
    out = df.copy()
    if "time" not in out.columns:
        out = out.reset_index()
    if "time" not in out.columns:
        out = out.rename_axis("time").reset_index()
    out["time"] = _utc_datetime_ns(out["time"])
    return out.sort_values("time").reset_index(drop=True)


def load_or_compute_gauge(
    station_code: str,
    start: str,
    end: str,
    nap_msl_offset_m: float = 0.0,
    overwrite: bool = False,
) -> tuple[pd.DataFrame, dict]:
    """Return cleaned gauge measurements and station metadata.

    Downloads water-level data (WATHTE, cm+NAP) from the RWS DDL archive via
    ddlpy, converts to metres+MSL, and caches the result.

    Parameters
    ----------
    station_code     : ddlpy location index (e.g. ``denhelder.marsdiep``) or legacy
                       code (e.g. ``DENHDR``) or part of the station name.
    start, end       : ISO date strings.
    nap_msl_offset_m : Subtract this from (cm/100) to convert NAP → MSL.
    overwrite        : If True, re-download even if cache exists.

    Returns
    -------
    (df, meta) where df has columns ``time``, ``water_level_cm_NAP``, ``water_level_m_MSL``
    and meta is a dict with ``lon``, ``lat``, ``name``, ``code``.
    """
    path = _cache_path("gauge", station_code, start, end)

    # Station metadata (coordinates) — look up from DDL catalogue regardless,
    # because it is fast and the coordinates do not change.
    import ddlpy
    all_locs = ddlpy.locations()
    wathte = all_locs[all_locs["Grootheid.Code"] == "WATHTE"]
    station = _resolve_gauge_station(wathte, station_code)
    row = station.iloc[0]
    resolved_code = str(station.index[0])
    # Coördinaten staan al als Lat/Lon (ETRS89 ≈ WGS84); geen RD-transformatie nodig.
    lon, lat = float(row["Lon"]), float(row["Lat"])
    meta = {"lon": lon, "lat": lat, "name": row.get("Naam", resolved_code), "code": resolved_code}

    if path.exists() and not overwrite:
        return _dataframe_with_time_column(_load(path)), meta

    print(f"Downloading WATHTE for {resolved_code} ({start} to {end}) ...")
    print("(ddlpy chunks the API calls automatically; typically 1–3 minutes.)")
    raw = ddlpy.measurements(row, start_date=start, end_date=end)
    val_col = _gauge_value_column(raw)
    gauge = (
        raw[[val_col]]
        .copy()
        .rename(columns={val_col: "water_level_cm_NAP"})
    )
    gauge.index = _utc_datetime_ns(gauge.index)
    gauge = gauge.sort_index()
    gauge["water_level_m_MSL"] = gauge["water_level_cm_NAP"] / 100.0 - nap_msl_offset_m
    gauge = gauge[gauge["water_level_m_MSL"].between(-5, 5)].dropna()
    _save(gauge, path)
    return _dataframe_with_time_column(gauge), meta


def tidal_coverage_stats(observed_heights, all_heights, min_observations: int = 3):
    """Bishop-Taylor-style coverage metrics from satellite vs full tide heights (m, MSL).

    Uses the same core logic as ``eo_tides.stats.tide_stats`` but accepts plain arrays
    (the tide heights already tagged in ``03_tides``).

    Returns a dict for the summary table, or ``None`` when there are too few observations.
    """
    import xarray as xr
    from eo_tides.stats import _tide_statistics

    obs = np.asarray(observed_heights, dtype=float)
    obs = obs[np.isfinite(obs)]
    all_h = np.asarray(all_heights, dtype=float)
    all_h = all_h[np.isfinite(all_h)]

    if len(obs) < min_observations or len(all_h) < 2:
        return None

    obs_da = xr.DataArray(obs, dims=("time",), coords={"time": np.arange(len(obs))})
    all_da = xr.DataArray(all_h, dims=("time",), coords={"time": np.arange(len(all_h))})
    s = _tide_statistics(obs_da, all_da).to_pandas()

    spread = float(s.spread)
    return {
        "observed_count": int(len(obs)),
        "observed_range": float(s.otr),
        "tot": spread,
        "hot": 1.0 - float(s.offset_high),
        "lot": 1.0 - float(s.offset_low),
        "spread": spread,
    }
