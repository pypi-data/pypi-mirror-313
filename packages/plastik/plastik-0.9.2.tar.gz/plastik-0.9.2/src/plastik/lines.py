"""Module that stores nice-to-have objects related to plotted lines."""

import itertools


def get_linestyle_dict() -> dict[str, str | tuple]:
    """Get back a dictionary of dense but non-solid line styles.

    Returns
    -------
    dict[str, str | tuple]
        Dictionary with a descriptive name and value of some nice and dense matplotlib
        line styles.

    Notes
    -----
    See <https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html>.
    """
    return {
        "dotted": (0, (1, 1)),  # :
        "dashed": (0, (3, 1)),  # --
        "dashdot": (0, (5, 1, 1, 1)),  # -.
        "long dash": (0, (6, 2)),
        "densely dashdotted": (0, (4, 2, 1, 2)),
        "densely dashdotdotted": (0, (3, 1, 1, 1, 1, 1)),
    }


def get_linestyle_cycle() -> itertools.cycle:
    """Get back an object cycling some dense but non-solid line styles.

    Returns
    -------
    itertools.cycle
        An object that will cycle matplotlib line styles.

    Examples
    --------
    >>> ls = get_linestyle_cycle()
    >>> next(ls)
    (0, (1, 1))

    >>> next(ls)
    (0, (3, 1))
    """
    return itertools.cycle(list(get_linestyle_dict().values()))
