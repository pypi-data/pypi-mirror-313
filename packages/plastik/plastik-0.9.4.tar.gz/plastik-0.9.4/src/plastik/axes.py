"""Manipulate the axis of matplotlib figures."""

import matplotlib as mpl
import matplotlib.pyplot as plt


def dark_theme(
    *ax: mpl.axes.Axes,
    fig: mpl.figure.Figure | None = None,
    keep_yaxis: bool = False,
) -> None:
    """Change plot style to fit a dark background.

    This is better in e.g. beamers with dark theme.

    Parameters
    ----------
    *ax : mpl.axes.Axes
        Send in any number of matplotlib axes and the changes will be applied to all
    fig : mpl.figure.Figure | None, optional
        The figure object that should be altered
    keep_yaxis : bool
        Keep the colour of the label along the vertical axis as is.
        Useful if a plot has y-labels that are coloured to match the plotted
        lines. Defaults to False.
    """
    for a in ax:
        if not keep_yaxis:
            a.tick_params(axis="both", colors="w")
            a.yaxis.label.set_color("w")
        else:
            a.tick_params(axis="x", colors="w")
        a.xaxis.label.set_color("w")
        plt.setp(a.spines.values(), color="gray")
    if fig is not None:
        fig.patch.set_alpha(0)
