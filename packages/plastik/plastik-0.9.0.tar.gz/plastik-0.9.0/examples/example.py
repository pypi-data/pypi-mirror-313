"""Example scripts for the `plastik` package."""

# General imports
import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from palettable.wesanderson import FantasticFox2_5

import plastik

SAVEDIR = pathlib.Path("examples/figures")
if not SAVEDIR.exists():
    SAVEDIR.mkdir(parents=True)

# Set the plotting style using the `default.mplstyle` file.
mpl.style.use("plastik.default")
# Log tick format -------------------------------------------------------------------- #


def _log_tick_format():
    # 1
    y = np.exp(np.linspace(-3, 5, 100))
    base = 2  # Default is 10, but 2 works equally well
    plt.figure()
    plt.semilogx(base=base)
    plt.plot(y)
    plt.savefig(SAVEDIR / "log_tick_format1.png")
    plastik.dark_theme(plt.gca(), fig=plt.gcf())
    plt.savefig(SAVEDIR / "log_tick_format1_dark.png")
    plt.show()
    plt.close("all")

    # 2
    y = np.exp(np.linspace(-3, 5, 100))
    base = 2  # Default is 10, but 2 works equally well
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.loglog(base=base)
    ax.plot(y)
    plt.savefig(SAVEDIR / "log_tick_format2.png")
    plastik.dark_theme(ax, fig=fig)
    plt.savefig(SAVEDIR / "log_tick_format2_dark.png")
    plt.show()
    plt.close("all")

    # 3
    y = np.exp(np.linspace(-3, 5, 100))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.semilogy(y)
    plt.savefig(SAVEDIR / "log_tick_format3.png")
    plastik.dark_theme(ax, fig=fig)
    plt.savefig(SAVEDIR / "log_tick_format3_dark.png")
    plt.show()
    plt.close("all")


# Topside legends -------------------------------------------------------------------- #


def _topside_legends():
    # 1
    y = np.linspace(-3, 5, 100)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(y, label="Topside legend 1")
    ax.plot(y + 1, label="Topside legend 2")
    ax.plot(y + 2, label="Topside legend 3")
    ax.plot(y + 3, label="Topside legend 4")
    plastik.topside_legends(ax, c_max=2, side="bottom", alpha=0.2)
    plt.savefig(SAVEDIR / "topside_legends1.png")
    plastik.dark_theme(ax, fig=fig)
    plt.savefig(SAVEDIR / "topside_legends1_dark.png")
    plt.show()
    plt.close("all")

    # 2
    y = np.linspace(-3, 5, 100)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(y, label="Topside legend 1")
    ax.plot(y + 1, label="Topside legend 2")
    ax.plot(y + 2, label="Topside legend 3")
    ax.plot(y + 3, label="Topside legend 4")
    plastik.topside_legends(ax, c_max=3, side="top right", alpha=1)
    plt.savefig(SAVEDIR / "topside_legends2.png")
    plastik.dark_theme(ax, fig=fig)
    plt.savefig(SAVEDIR / "topside_legends2_dark.png")
    plt.show()
    plt.close("all")


# Ridge ------------------------------------------------------------------------------ #


def _ridge():  # noqa: PLR0915
    # Set up
    x = np.linspace(1e-1, 3e1, 1000) ** 2

    def func(x, s):
        return 10 / ((x - s) ** 2 + 1)

    dt = [func(x, 3), func(x, 1), func(x, 0), func(x, 100), func(x, 300), func(x, 500)]
    dta = [(x, y) for y in dt]

    lab = [f"{i}" for i in range(6)]

    # 1
    r = plastik.Ridge(dta, "gsz", xlabel="bottom", ylabel="xlabel")
    r.main()
    f = r.figure
    ell = r.lines
    a = r.top_axes
    axs = r.all_axes
    a.legend(ell, lab)
    plt.savefig(f"{SAVEDIR}/ridge1.png")
    plastik.dark_theme(r.bottom_axes, keep_yaxis=True, fig=f)
    plastik.dark_theme(r.ax)
    plt.savefig(SAVEDIR / "ridge1_dark.png")
    plt.show()
    plt.close("all")

    # 2
    r = plastik.Ridge(dta, "gs", ylabel="xlabel")
    r.main()
    f = r.figure
    ell = r.lines
    a = r.top_axes
    axs = r.all_axes
    a.legend(ell, lab)
    plastik.topside_legends(a, ell, c_max=6, side="right")
    for ax in axs:
        ax.semilogy()
    plt.savefig(SAVEDIR / "ridge2.png")
    plastik.dark_theme(r.bottom_axes, keep_yaxis=True, fig=f)
    plastik.dark_theme(r.ax)
    plt.savefig(SAVEDIR / "ridge2_dark.png")
    plt.show()
    plt.close("all")

    # 3
    r = plastik.Ridge(
        dta, "s", xlabel="bottom axis label", ylabel="xlabel", pltype="semilogx"
    )
    r.main()
    f = r.figure
    ell = r.lines
    a = r.top_axes
    axs = r.all_axes
    a.legend(ell, lab)
    plastik.topside_legends(a, ell, c_max=5, side="right")
    for ax in axs:
        ax.semilogx()
    plt.savefig(SAVEDIR / "ridge3.png")
    plastik.dark_theme(r.bottom_axes, keep_yaxis=True, fig=f)
    plastik.dark_theme(r.ax)
    plt.savefig(SAVEDIR / "ridge3_dark.png")
    plt.show()
    plt.close("all")

    # 4
    r = plastik.Ridge(dta, "bz", ylabel="xlabel", pltype="loglog")
    r.main()
    f = r.figure
    a = r.bottom_axes
    axs = r.all_axes
    for ax in axs:
        ax.loglog()
    plt.savefig(SAVEDIR / "ridge4.png")
    plastik.dark_theme(r.bottom_axes, keep_yaxis=True, fig=f)
    plastik.dark_theme(r.ax)
    plt.savefig(SAVEDIR / "ridge4_dark.png")
    plt.show()
    plt.close("all")


# Dark theme ------------------------------------------------------------------------- #


def _dark_theme():
    # 1
    y = np.exp(np.linspace(-3, 5, 100))
    plt.figure()
    # Sets axes and labels of given axis to white
    plastik.dark_theme(plt.gca())
    plt.loglog(base=2)
    plt.plot(y)
    plt.xlabel("white label")
    plt.ylabel("ylabel")
    plt.savefig(SAVEDIR / "dark_theme.png")
    plt.show()
    plt.close("all")


# Color map -------------------------------------------------------------------------- #
def _color_map():
    plastik.colors.palettable_help()
    plastik.colors.make_color_swatch(
        plt.figure(figsize=(12, 3)).gca(),
        FantasticFox2_5.hex_colors,
    )
    prints = plastik.colors.create_colorlist("gist_rainbow", 20)
    print(prints)
    color_map = plastik.colors.create_colorlist("gist_rainbow", 20, map=True)
    # First 5 colors in the map
    first_five = [mpl.colors.to_hex(c) for c in color_map(range(5))]
    print(first_five)
    # All 20 colors in the map, with the last one repeated 30 times
    print([mpl.colors.to_hex(c) for c in color_map(range(50))])
    # All colors in the map
    color_list = [mpl.colors.to_hex(c) for c in color_map(range(20))]
    print(all(j == k for j, k in zip(prints, color_list, strict=False)))  # True
    # A new map based on raw input (first five from gist_rainbow, n=20) is created and
    # samples are drawn from it.
    print(first_five)
    print(plastik.colors.create_colorlist(first_five, 20))

    custom_colors = ["#123456", "#654321", "#fedcba", "#abcdef", "#aa11aa", "#11aa11"]
    custom_colors_map = plastik.colors.create_colorlist(custom_colors, 20, map=True)
    print([mpl.colors.to_hex(c) for c in custom_colors_map(range(20))])

    # Plot the colors
    # As a color swatch 1
    plt.figure()
    plastik.colors.make_color_swatch(plt.gca(), color_map)
    # As a color swatch 2
    plt.figure()
    plastik.colors.make_color_swatch(plt.gca(), color_map, no_ticks=True, resolution=7)
    # As a color swatch 3
    plt.figure()
    plastik.colors.make_color_swatch(plt.gca(), color_map, no_border=True, ratio=50)
    # As an inset with other data
    plt.figure()
    ax = plt.gca()
    x0, y0, width, height = 0.52, 0.8, 0.40, 0.25
    ax.scatter(
        np.arange(20),
        np.ones(20),
        c=custom_colors_map(range(20)),
    )
    ax2 = ax.inset_axes((x0, y0, width, height))
    ax2 = plastik.colors.make_color_swatch(
        ax2, custom_colors_map, no_ticks=False, ratio=5
    )
    ax2.set_xticks((0, 30, 60, 90), (0, "hey", True, 2), size=6)  # type: ignore[arg-type]
    ax2.set_yticks([])
    plt.show()

    # And as our final trick, let us use a pre-defined colour palette for a section of
    # the colour map, in addition to adding in some of our own.
    viridis = plastik.colors.create_colorlist("cmc.batlow", 14)
    v_check = plastik.colors.create_colorlist(viridis, 14)
    v_check2 = plastik.colors.create_colorlist([viridis[0], viridis[-1]], 14)
    print(viridis)  # True viridis (by definition)
    print(v_check)  # True viridis (equivalent to above)
    print(v_check2)  # Incorrect (fills in between according to a different method)
    # Now combine viridis with some random colours.
    custom = viridis.copy()
    for _ in range(3):
        custom.append("#6543ff")
    for _ in range(3):
        custom.insert(0, "#2eff2e")
    # Plot the color_map alone.
    plt.figure(figsize=(10, 1), layout="constrained")
    plastik.colors.make_color_swatch(plt.gca(), custom, no_ticks=False)
    # As an inset with other data
    fig2 = plt.figure()
    ax = plt.gca()
    x0, y0, width, height = 0.57, 0.87, 0.40, 0.1
    ax.scatter(
        np.arange(len(custom)),
        np.ones(len(custom)),
        c=custom,
    )
    ax2 = ax.inset_axes((x0, y0, width, height))
    plastik.colors.make_color_swatch(ax2, custom, ratio=2 * len(custom))
    ax2.set_xticks((0, 3, 6, 17, 20), (0, "Zzz", "See", "Stop", 2), rotation=20, size=6)  # type: ignore[arg-type]
    fig2.savefig(SAVEDIR / "color_map.png")
    plt.show()


# Figure grid ------------------------------------------------------------------------ #
def _figure_grid():
    fig1, axs1 = plastik.figure_grid(2, 2)
    for i, ax in enumerate(axs1):
        ax.plot(np.array([1, 2, 3]), np.array([1, 2, 3]) * i)
    fig1.savefig(SAVEDIR / "figure_grid_default.png")
    # For further customisation of the text, use the class directly and the `get_grid`
    # method with `kwargs`. You can for example change the anchor point of the text.
    fig2, axs2 = plastik.figure_grid(
        2,
        2,
        {
            "labels": ["Hello subplot title", 1, r"$4\hbar$", None],
            "pos": (0.6, 0.1),
            "share_axes": "x",
            "columns_first": True,
        },
    )
    for i, ax in enumerate(axs2):
        ax.plot(np.array([1, 2, 3]), np.array([1, 2, 3]) * i)
    fig2.savefig(SAVEDIR / "figure_grid_opts.png")
    plt.show()


# Airport ---------------------------------------------------------------------------- #
def _airport():
    t = np.linspace(0, 1, 101)
    a = np.exp(t) + np.random.default_rng().normal(size=101) / 3
    b = np.exp(t) + np.random.default_rng().normal(size=101) / 3 + 0
    rnd = np.random.default_rng().normal(size=101)
    ax1 = (fig1 := plt.figure()).gca()
    plastik.airport(
        a,
        b,
        rnd,
        ax1,
        labels=("$b-a$", "Control", None),
        ax_labels=("Array: $a$ [Unit]", "Array: $b$ [Unit]", r"$\Delta$ Unit"),
    )
    fig1.savefig(SAVEDIR / "airport_default.png")
    ax2 = (fig2 := plt.figure()).gca()
    ap = plastik.Airport()
    ap.config(distribution_xline=1, runway_data_kwargs={"c": "red", "marker": "s"})
    ap.plot(a, b, rnd, ax2)
    fig2.savefig(SAVEDIR / "airport_configured.png")
    plt.show()


if __name__ == "__main__":
    _log_tick_format()
    _topside_legends()
    _ridge()
    _dark_theme()
    _color_map()
    _figure_grid()
    _airport()
