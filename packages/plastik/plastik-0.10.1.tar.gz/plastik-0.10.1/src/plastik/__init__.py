"""Library for creating beautiful and insightful visualizations."""

import importlib.metadata
from importlib.metadata import version

from plastik import colors, lines
from plastik.axes import *  # noqa:F401,F403
from plastik.grid import *  # noqa:F401,F403
from plastik.legends import *  # noqa:F401,F403
from plastik.percentiles import percentiles
from plastik.ridge import *  # noqa:F401,F403

try:
    from plastik.airport import Airport, airport
except importlib.metadata.PackageNotFoundError:
    # We were not able to find the package `fppanalysis`

    def need_extra(*_, **k):
        raise ImportError(
            "Please install with extra dependencies: `pip install plastik[extra]`"
        )

    Airport = need_extra  # type: ignore[misc,assignment]
    airport = need_extra  # type: ignore[assignment]
except ImportError:
    # We were not able to find the correct version of the package `fppanalysis`

    def need_extra(*_, **k):
        raise ImportError(
            "The package 'fppanalysis' cannot be at version 0.1.4. You may want to "
            "explicitly install it to your project as "
            "`git+https://github.com/uit-cosmo/fpp-analysis-tools@main`."
        )

    Airport = need_extra  # type: ignore[misc,assignment]
    airport = need_extra  # type: ignore[assignment]

__version__ = version(__package__)
__all__ = ["Airport", "airport", "colors", "lines", "percentiles"]
