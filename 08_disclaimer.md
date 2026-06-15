---
title: Disclaimer & credits
short_title: Disclaimer
execute:
  skip: true
---

# Disclaimer & credits

This tutorial was developed for the **NCK** (Netherlands Centre for Coastal Research) summer school in Texel from 15th to 26th of June.
Keep in mind that this is **educational material** — a hands-on introduction, not an operational mapping product.

---

## Course contacts

This course is developed by Dr Tim Grandjean [tim.grandjean@nioz.nl](mailto:tim.grandjean@nioz.nl) and Prof. Dr Daphne van der Wal [Daphne.van.der.Wal@nioz.nl](mailto:Daphne.van.der.Wal@nioz.nl). 

---

## Continuing beyond the course

We are happy to **share knowledge and methods** — that is why this material is open. If you
want to **take the data further** in a scientific context, we would **welcome being
involved** in those follow-up steps. That can mean a short check-in on your approach, co-supervision, or collaboration — especially when results may inform management or publication.
**Get in touch early** rather than after months of solo work; it saves time and avoids
reinventing wheels.

---

## Methodological context

The elevation workflow (**page 6**) builds on the open **DEA Intertidal** algorithm
(`intertidal.elevation()`), developed by **Bishop-Taylor** and colleagues at Geoscience
Australia — NDWI tagged with modelled tide height, crossover height as elevation.

NIOZ-related work on **tidal-flat dynamics from satellite** — including time-series elevation
and morphological change — connects to research by **Grandjean**, **van der Wal**, and
collaborators (e.g. *Nature Geoscience*, 2024 on turbidity and flat maintenance). The
**Applications** page points in that direction; the underlying papers and software are the
scientific references for those methods, not this tutorial itself.

---

## Practical notes

Tutorial text and notebooks can be found at the [GitHub repository](https://github.com/timgrandjean93/NCK-TidalFlat). All satellite data and DEA software carry their own licences.

| Data / tool in this tutorial | Source |
|---|---|
| **DEA Intertidal** | [Geoscience Australia](https://github.com/GeoscienceAustralia/dea-intertidal) |
| **FES2022** | [AVISO+ / CNES](https://www.aviso.altimetry.fr/en/data/products/auxiliary-products/global-tide-fes.html) |
| **Planetary Computer** | Microsoft STAC / Landsat access |
| **RWS gauges (page 4)** | Rijkswaterstaat via `rws-ddlpy` |
