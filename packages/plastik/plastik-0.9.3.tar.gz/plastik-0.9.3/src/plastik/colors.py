"""Module for working with colours."""

import inspect
import sys
from collections.abc import Sequence
from typing import Literal, overload

import cmcrameri  # noqa
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import palettable  # noqa
import pywaffle


@overload
def create_colorlist(
    color_specifier: Sequence | str, n: int, map: Literal[False] = False
) -> list[str]: ...


@overload
def create_colorlist(
    color_specifier: Sequence | str, n: int, map: Literal[True]
) -> mpl.colors.Colormap: ...


def create_colorlist(
    color_specifier: Sequence | str, n: int, map: bool = False
) -> list[str] | mpl.colors.Colormap:
    """Create `n` colors from a color map.

    The `n` colours are drawn from one of the matplotlib colour maps, or a new colour
    map is created using the input colours. Specifying 'help' as the ``color_specifier``
    will print the list of available colour names in a nicer format.

    Parameters
    ----------
    color_specifier : Sequence | str
        The name of a matplotlib colour map or a list of two colors. To get the full
        list of available color maps, try with a nonsense color map, or see
        https://matplotlib.org/stable/tutorials/colors/colormaps.html#classes-of-colormaps.
        If two colors in a list is provided, any color that
        ``matplotlib.colors.LinearSegmentedColormap.from_list`` accepts is valid. You
        may also use the special name 'help' to get a list of available colour names.
    n : int
        The number of colors to be created.
    map : bool
        If True, return the colour map itself instead of the list. To draw colours from
        it, use ``color_map(range(n))``, or to place HEX values in a list::

            import matplotlib.colors as mpl.colors
            n = 5
            c_list = [mpl.colors.to_hex(c) for c in color_map(range(n))]

    Returns
    -------
    list[str] | mpl.colors.Colormap
        A list of `n` colors in HEX format.

    Raises
    ------
    AttributeError
        If the type of the ``color_specifier`` is not recognized.

    See Also
    --------
    `Palettable<https : //jiffyclub.github.io/palettable/#documentation>`_ is a collection
    of predefined colour maps that include the matplotlib colours, cmcrameri colours and
    many more (colour maps from the Wes Anderson movies being one of them!). Let us look
    at an example : :

        import matplotlib.pyplot as plt
        from palettable.wesanderson import Moonrise1_5 as wes_clr
        import plastik
        plastik.colors.make_color_swatch(
            plt.figure(figsize=(12, 3)).gca(),
            wes_clr.hex_colors,
        )

    cosmoplots.generate_hex_colors : Color generator based on standard colour maps.

    Note
    ----
    With `colour<https://github.com/vaab/colour>`_ we can do it like this::

        import colour
        c_grad = [
            c.get_hex()
            for c in list(colour.Color(start_c).range_to(colour.Color(main_c), n))
        ]

    But, the project is old (last commit on 19 Nov 2017), so let us do it with
    ``matplotlib.colors`` instead. The results are not identical, but who knows
    which is better.
    """
    if isinstance(color_specifier, list):
        return _create_colorlist_between(color_specifier, n, map=map)
    elif isinstance(color_specifier, str):
        return _create_colorlist_from(color_specifier, n, map=map)
    raise AttributeError("'color_specifier' must be either a list or a string.")


def _create_colorlist_from(
    cmap_name: str, n: int, map: bool = False
) -> list[str] | mpl.colors.Colormap:
    """Create `n` colors that are drawn from one of the matplotlib color maps.

    Parameters
    ----------
    cmap_name : str
        The name of a matplotlib color map. To get the full list of available color
        maps, try with a nonsense color map, or see
        https://matplotlib.org/stable/tutorials/colors/colormaps.html#classes-of-colormaps.
    n : int
        The number of colors to be created.
    map : bool
        If True, return the color map itself instead of the list. To draw colors from
        it, use ``color_map(range(n))``, or to place HEX values in a list::

            import matplotlib.colors as mpl.colors
            n = 5
            c_list = [mpl.colors.to_hex(c) for c in color_map(range(n))]

    Returns
    -------
    list[str] | mpl.colors.Colormap
        A list of `n` colors in HEX format.
    """
    if cmap_name == "help":
        try:
            plt.get_cmap(cmap_name, 1)
        except Exception as e:
            s1, s2 = str(e).split(" supported values are ")
            print("Supported colour names are:")
            for word in s2.split(", "):
                word_ = word[1:-1]
                if word_.startswith("cmc"):
                    print("\t", word_, "\t(from cmcrameri)")
                else:
                    print("\t", word_)
        sys.exit()
    if map:
        return plt.get_cmap(cmap_name, n)
    return [mpl.colors.to_hex(c) for c in plt.get_cmap(cmap_name, n)(range(n))]


def _create_colorlist_between(
    colors: Sequence, n: int, map: bool = False
) -> list[str] | mpl.colors.LinearSegmentedColormap:
    """Create `n` colors between two colors (inclusive).

    Parameters
    ----------
    colors : Sequence
        The full sequence of colours we should create a colour list from. It should
        contain ``str`` objects, but we could have accepted more types here, since
        anything that ``matplotlib.colors.LinearSegmentedColormap.from_list`` accepts is
        valid.
    n : int
        The length of the list of colours from the colour map.
    map : bool
        If True, return the color map itself instead of the list. To draw colors from
        it, use ``color_map(range(n))``, or to place HEX values in a list::

            import matplotlib.colors as mpl.colors
            n = 5
            c_list = [mpl.colors.to_hex(c) for c in color_map(range(n))]

    Returns
    -------
    list[str] | mpl.colors.LinearSegmentedColormap
        The hex values of all generated colors.
    """
    if map:
        return mpl.colors.LinearSegmentedColormap.from_list("Custom", colors, N=n)
    return [
        mpl.colors.to_hex(c)
        for c in mpl.colors.LinearSegmentedColormap.from_list("Custom", colors, N=n)(
            range(n)
        )
    ]


def palettable_help() -> None:
    """Print helt text about the `palettable` package."""
    print(
        "This package includes `palettable` as a dependency, but do not implement any"
        " of its colour maps. Rather, have a look at their documentation at"
        " https://jiffyclub.github.io/palettable/#documentation and use it as its own"
        " package. "
    )
    print(
        "Integrating it with `plastik` is simple, just load any palette, and for"
        " example call the `hex_colors` attribute they all have (again, see the"
        " `palettable` documentation). This is a list of HEX colours that can then be"
        " given to `make_color_swatch`."
    )
    print(
        "And just to tease you a bit more, here is a list of the available colour"
        " palette modules:"
    )
    for i in inspect.getmembers(palettable, inspect.ismodule):
        if i[0] not in ["utils", "palette"]:
            print("\t", i[0])


def make_color_swatch(  # noqa: PLR0913
    ax: mpl.axes.Axes,
    c_bar: mpl.colors.Colormap | list[str],
    vertical: bool = False,
    resolution: int = 90,
    ratio: int = 8,
    no_border: bool = False,
    no_ticks: bool = True,
) -> mpl.axes.Axes:
    """Create a color swatch on the given axis object from the given color map.

    Parameters
    ----------
    ax : mpl.axes.Axes
        The axis object to create the colour bar on.
    c_bar : mpl.colors.Colormap | list[str]
        A color map to draw colors from or a list of all colour that should be used.
    vertical : bool
        Whether the colours in the colour bar should be vertically or horizontally
        aligned. Default is False, a horizontal alignment. Only used when ``c_bar`` is a
        ``list``.
    resolution : int
        The horizontal resolution / density of the color gradient. Only used when
        ``cmap`` is a ``mpl.colors.Colormap``.
    ratio : int
        The vertical-to-horizontal ratio of one individual colour in the colour swatch.
        Only used when ``cmap`` is a ``mpl.colors.Colormap``. (The ratio can at the
        moment only be made 1:1, or slimmer). When ``cmap`` is a ``list``, the figure
        size or axis size defines the total width and height of the colour swatch.
    no_border : bool
        Remove all borders. Takes precedence over ``no_ticks``. Default is ``False``.
        See ``plt.Axes.set_axis_off``.
    no_ticks : bool
        Remove all tick marks, but keep the border. Default is ``True``. See
        ``plt.Axes.set_xticks`` and ``plt.Axes.set_yticks``.

    Returns
    -------
    mpl.axes.Axes
        Return the input axes object.

    Examples
    --------
    Let us create a figure that uses the function to create its colour bar. We here use
    a pre-defined colour palette for a section of the colour map, in addition to adding
    in some of our own colours.

    >>> viridis = plastik.colors.create_colorlist("viridis", 14)

    Now combine viridis with some random colours.

    >>> custom = viridis.copy()
    >>> for _ in range(3):
    ...     custom.append("#6543ff")
    >>> for _ in range(3):
    ...     custom.insert(0, "#2eff2e")

    Plot the ``color_map`` alone. The ``figsize`` parameter exactly defines the shape of
    the colour swatch.

    >>> plt.figure(figsize=(10, 1), layout="constrained")
    >>> plastik.colors.make_color_swatch(plt.gca(), custom, no_ticks=False)

    Then, as an inset with other data.

    >>> plt.figure()
    >>> ax = plt.gca()
    >>> x0, y0, width, height = 0.52, 0.8, 0.40, 0.15
    >>> ax.scatter(
    ...     np.arange(len(custom)),
    ...     np.ones(len(custom)),
    ...     c=custom,
    ... )
    >>> ax2 = ax.inset_axes([x0, y0, width, height])
    >>> ax2 = plastik.colors.make_color_swatch(
    ...     ax2, custom, ratio=2 * len(custom), no_border=True
    ... )

    You can make a custom label with the returned axis element's ``set_xticks`` (or
    ``set_yticks``), where ``length`` is the length of the given ``c_bar`` list or equal
    to the resolution.

    >>> length = len(custom)
    >>> ax2.set_xticks(list(range(length)), [f"No: {i}" for i in range(length)])
    >>> plt.show()
    """
    if isinstance(c_bar, list):
        row_col = "columns" if vertical else "rows"
        kwarg = {row_col: 1}
        pywaffle.Waffle.make_waffle(
            ax=ax,
            values=[1 for _ in range(len(c_bar))],
            colors=c_bar,
            interval_ratio_x=0,
            interval_ratio_y=0,
            starting_location="NW",
            vertical=True,
            block_arranging_style="snake",
            tight={"pad": 0},
            **kwarg,
        )
        ax.set_axis_on()
    else:
        gradient = np.linspace(0, 1, resolution)
        if resolution // ratio < 1:
            print(
                f"The resolution cannot be less than the ratio (={ratio}). Setting"
                f" {resolution = } -> {ratio}"
            )
            resolution = ratio
        gradient = np.vstack(tuple(gradient for _ in range(int(resolution // ratio))))
        ax.imshow(
            gradient,
            cmap=c_bar,
            interpolation="nearest",
            origin="lower",
        )
    if no_ticks:
        ax.set_xticks([])
        ax.set_yticks([])
    if no_border:
        ax.set_axis_off()
    return ax
