# circle_detection

### A Python Package for Detecting Circles in 2D Point Sets.

![pypi-image](https://badge.fury.io/py/circle-detection.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/josafatburmeister/circle_detection/actions/workflows/code-quality-main.yml/badge.svg)](https://github.com/josafatburmeister/circle_detection/actions/workflows/code-quality-main.yml)
[![coverage](https://codecov.io/gh/josafatburmeister/circle_detection/branch/main/graph/badge.svg)](https://codecov.io/github/josafatburmeister/circle_detection?branch=main)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/circle_detection)

The package allows to detect circles in a set of 2D points using the M-estimator method proposed in [Garlipp, Tim, and Christine H. Müller. "Detection of Linear and Circular Shapes in Image Analysis." Computational Statistics & Data Analysis 51.3 (2006): 1479-1490.](<https://doi.org/10.1016/j.csda.2006.04.022>)

### Get started

The package can be installed via pip:

```bash
python -m pip install circle-detection
```

The package provides a method ```detect_circles```, which can be used as follows:

```python
from circle_detection import detect_circles
import numpy as np

xy = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]], dtype=np.float64)

detected_circles, fitting_losses = detect_circles(xy, bandwidth=0.05, max_circles=1)

if len(detected_circles) > 0:
    circle_center_x, circle_center_y, circle_radius = detected_circles[0]
```

### Package Documentation

The package documentation is available [here](https://josafatburmeister.github.io/circle_detection/stable).
