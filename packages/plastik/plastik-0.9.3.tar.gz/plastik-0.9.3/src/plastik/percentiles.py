"""Module for plotting percentiles from an ensemble of arrays."""

from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def percentiles(  # noqa: PLR0913
    x: np.ndarray,
    y: np.ndarray,
    n: int = 20,
    ax: mpl.axes.Axes | None = None,
    plot_mean: bool = False,
    plot_median: bool = True,
    **kwargs: Any,
) -> mpl.axes.Axes:
    """Calculate percentiles from ensemble 'y' along 'x'.

    Parameters
    ----------
    x : np.ndarray
        One dimensional array, x-axis.
    y : np.ndarray
        Values along y-axis. Need shape (N, len(x)).
    n : int
        The number of percentiles, linearly spaced from 50 to 'percentile_m{in,ax}'.
        Defaults to 20.
    ax : mpl.axes.Axes | None, optional
        The axes object to plot on. If not given, the current axes will be used.
    plot_mean : bool
        Plot mean of 'y'
    plot_median : bool
        Plot median of 'y'
    **kwargs : Any
        alpha : str
            Alpha value of each layer of the percentiles
        color : str
            Colour of the percentile shading. Can be any colour that can be parsed by
            matplotlib's plotting function.
        line_color : str
            Colour of the mean/median plot. Can be any colour that can be parsed by
            matplotlib's plotting function.
        percentile_min : float
            Lower percentile limit.
        percentile_max : float
            Upper percentile limit.

    Returns
    -------
    mpl.axes.Axes
        The axes object of the figure.
    """
    ax = ax or plt.gca()
    # calculate the lower and upper percentile groups, skipping 50 percentile
    percentile_min = kwargs.pop("percentile_min") if "percentile_min" in kwargs else 1
    percentile_max = kwargs.pop("percentile_max") if "percentile_max" in kwargs else 99
    perc1 = np.percentile(
        y, np.linspace(percentile_min, 50, num=n, endpoint=False), axis=0
    )
    perc2 = np.percentile(y, np.linspace(50, percentile_max, num=n + 1)[1:], axis=0)

    color = kwargs.pop("color") if "color" in kwargs else "r"
    line_color = kwargs.pop("line_color") if "line_color" in kwargs else "k"
    if plot_mean:
        ax.plot(x, np.mean(y, axis=0), color=line_color)

    if plot_median:
        ax.plot(x, np.median(y, axis=0), "-d", color=line_color)

    alpha = kwargs.pop("alpha") if "alpha" in kwargs else 1 / n
    # fill lower and upper percentile groups
    for p1, p2 in zip(perc1, perc2, strict=True):
        ax.fill_between(x, p1, p2, alpha=alpha, color=color, edgecolor=None)

    return ax
