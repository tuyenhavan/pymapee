# pymapee


[![image](https://img.shields.io/pypi/v/pymapee.svg)](https://pypi.python.org/pypi/pymapee)
[![image](https://img.shields.io/conda/vn/conda-forge/pymapee.svg)](https://anaconda.org/conda-forge/pymapee)

[![image](https://pyup.io/repos/github/tuyenhavan/pymapee/shield.svg)](https://pyup.io/repos/github/tuyenhavan/pymapee)


**A Simple Python package to pre-processing satellite data using Google Earth Engine.**

`pymapee` is a simple Python package that aims to provide common functionalities to pre-process or calculate vegetation drought indices using Google Earth Engine. Currently, this package supports cloud masking (MODIS, Landsat, Sentinel-2), composite (monthly), and calculation of vegetation anomaly index (VAI) and vegetation condition index (VCI). It also supports to download an image collection (e.g., time-series NDVI or LST) or an image. This package is under active development, and changes are expected over time.

-  GitHub repo: [https://github.com/tuyenhavan/pymapee](https://github.com/tuyenhavan/pymapee)
-   Free software: MIT license
---
## Features

-   Masking cloud-related pixels (e.g., MODIS, Landsat, and Sentinel-2)
-   Making monthly composite
-   Calculating monthly vegetation anomaly index (VAI) and vegetation condition index (VCI).
-   Scaling data
-   Downloading an image or image collection (e.g., time-series NDVI)
---
## Installation
Install `pymapee` using pip 

`pip install pymapee`

or install from Github

`pip install git+https://github.com/tuyenhavan/pymapee.git`

---
## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
