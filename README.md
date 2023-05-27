# Welcome to pymapee

[![image](https://img.shields.io/pypi/v/pymapee.svg)](https://pypi.python.org/pypi/pymapee)
[![image](https://img.shields.io/conda/vn/conda-forge/pymapee.svg)](https://anaconda.org/conda-forge/pymapee)
[![image](https://pepy.tech/badge/pymapee)](https://pepy.tech/project/pymapee)
[![image](https://github.com/tuyenhavan/pymapee/workflows/docs/badge.svg)](https://pymapee.org)
[![image](https://github.com/tuyenhavan/pymapee/workflows/build/badge.svg)](https://github.com/tuyenhavan/pymapee/actions?query=workflow%3Abuild)
[![image](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


**A Simple Python package to pre-processing satellite-based data using Google Earth Engine.**

`pymapee` is a simple Python package that aims to provide common functionalities to pre-process or calculate vegetation drought indices using Google Earth Engine. Currently, this package supports cloud masking (MODIS, Landsat, Sentinel-2), composite (monthly), and calculation of vegetation anomaly index (VAI) and vegetation condition index (VCI). It also supports to download an image collection (e.g., time-series NDVI or LST) or an image. This package is under active development, and changes are expected over time.

-  GitHub repo: [https://github.com/tuyenhavan/pymapee](https://github.com/tuyenhavan/pymapee)
-   Free software: MIT license
---
## Features

-   Masking cloud-related pixels (e.g., MODIS, Landsat, and Sentinel-2)
-   Making monthly composite
-   Calculating monthly vegetation anomaly index (VAI) and vegetation condition index (VCI).
-   Interpolating time-series using linear interpolation
-   Scaling data
-   Downloading an image or image collection (e.g., time-series NDVI)

Examples are provided [here](https://github.com/tuyenhavan/pymapee/tree/main/examples), and it will be regularly updated.

---
## Installation
Install `pymapee` using pip 

`pip install pymapee`

or install from Github to get the latest update.

`pip install git+https://github.com/tuyenhavan/pymapee.git`

---
## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.

