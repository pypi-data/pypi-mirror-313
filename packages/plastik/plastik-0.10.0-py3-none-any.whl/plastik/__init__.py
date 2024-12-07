"""Library for creating beautiful and insightful visualizations."""

from importlib.metadata import version

from plastik import colors, lines
from plastik.axes import *  # noqa:F401,F403
from plastik.grid import *  # noqa:F401,F403
from plastik.legends import *  # noqa:F401,F403
from plastik.percentiles import percentiles
from plastik.ridge import *  # noqa:F401,F403

try:
    from plastik.airport import Airport, airport
except ImportError:

    def need_extra(*_, **k):
        raise ImportError(
            "Please install with extra dependencies: pip install plastik[extra]"
        )

    Airport = need_extra  # type: ignore[misc,assignment]
    airport = need_extra  # type: ignore[assignment]

__version__ = version(__package__)
__all__ = ["Airport", "airport", "colors", "lines", "percentiles"]
