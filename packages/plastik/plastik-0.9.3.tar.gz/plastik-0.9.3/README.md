# plastik

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> plt assist, plastic surgery for plt

## Install

`plastik` is available through [PyPI]:

```bash
pip install plastik
```

Installing the development version is done using [uv]:

```bash
git clone https://github.com/engeir/plastik.git
cd plastik
uv sync
```

## Usage

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import plastik

mpl.style.use("plastik.default")
fig, axs = plastik.figure_grid(
    2,
    2,
    {
        "labels": ["Hello subplot title", 1, r"$4\hbar$", None],
        "pos": (0.6, 0.1),
        "share_axes": "x",
        "columns_first": True,
    },
)
for i, ax in enumerate(axs):
    ax.plot(np.array([1, 2, 3]), np.array([1, 2, 3]) * i)
fig.savefig("figure_grid_opts.png")
plt.show()
```

See more [examples](./examples/example.py) and their
[output](https://github.com/engeir/plastik/pull/24/files).

[PyPI]: https://pypi.org/
[uv]: https://docs.astral.sh/uv/
