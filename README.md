# Create-simple-map-in-VS-Code
PyGMT-based Python script for generating high-resolution bathymetric maps of marine sampling sites, with Spratelloides gracilis sites included as an example dataset.
# Marine Sampling Site Bathymetric Map (PyGMT)

This repository contains a Python script for generating high-resolution, publication-quality bathymetric maps of marine sampling sites using PyGMT.

The included *Spratelloides gracilis* dataset serves only as an example. The script is fully customizable and can be used for **any species or geographic dataset**.

---

## ✨ Features

- Reads sampling coordinates from a CSV file
- Automatically assigns marker styles and colors
- Uses high-resolution Earth relief bathymetry (30 arc-second)
- Applies a continuous depth gradient colormap
- Adds:
  - Geographic labels (e.g., island groups or regions)
  - Ocean/sea labels
  - Scale bar and north arrow
  - Custom legend for sampling sites
- Outputs a **600 dpi publication-ready PNG**

---

## 📂 Input Requirements

CSV file must contain:

```text
Longitude
Latitude
