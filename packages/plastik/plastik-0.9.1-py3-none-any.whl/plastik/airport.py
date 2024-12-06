"""Create an airport-plot on a ``matplotlib.axes.Axes`` object."""

from collections.abc import Callable

import fppanalysis
import matplotlib as mpl
import numpy as np
import scipy
from numpy.typing import NDArray


class Airport:
    """Create an airport-plot."""

    def _setup(
        self,
        arr1: NDArray[np.float64],
        arr2: NDArray[np.float64],
        control: NDArray[np.float64],
        labels: tuple[str | None, str | None, str | None] = (
            "Arr2-Arr1",
            "Control",
            "Runway data",
        ),
        ax_labels: tuple[str, str, str] = (
            "X label",
            "Y label",
            "Distribution X label",
        ),
    ) -> None:
        self.arr1 = arr1
        self.arr2 = arr2
        self.control = control
        self.labels = labels
        self.ax_labels = ax_labels
        self.bins = 30
        self.dist_func_discrete = self.dist_func_discrete_pdf
        self.dist_func_continuous = self.dist_func_continuous_pdf

    def __call__(  # noqa: PLR0913
        self,
        arr1: NDArray[np.float64],
        arr2: NDArray[np.float64],
        control: NDArray[np.float64],
        ax: mpl.axes.Axes,
        labels: tuple[str | None, str | None, str | None] = (
            "Arr2-Arr1",
            "Control",
            "Runway data",
        ),
        ax_labels: tuple[str, str, str] = (
            "X label",
            "Y label",
            "Distribution X label",
        ),
    ) -> mpl.axes.Axes:
        """Create an airport-plot with default settings."""
        self.config()
        self._setup(arr1, arr2, control, labels, ax_labels)
        return self._plot(ax)

    def plot(  # noqa: PLR0913
        self,
        arr1: NDArray[np.float64],
        arr2: NDArray[np.float64],
        control: NDArray[np.float64],
        ax: mpl.axes.Axes,
        labels: tuple[str | None, str | None, str | None] = (
            "Arr2-Arr1",
            "Control",
            "Runway data",
        ),
        ax_labels: tuple[str, str, str] = (
            "X label",
            "Y label",
            "Distribution X label",
        ),
    ):
        """Create an airport-plot with the current settings."""
        self._setup(arr1, arr2, control, labels, ax_labels)
        self._plot(ax)

    def config(  # noqa: PLR0913
        self,
        *,
        bins: int = 30,
        distribution_scaling: float = 1.0,
        distribution_xline: float = 0.9,
        runway_end: float = 1.35,
        runway_start: float = -0.05,
        runway_data_kwargs: dict | None = None,
        dist_data_kwargs: dict | None = None,
        dist_ctrl_kwargs: dict | None = None,
    ) -> None:
        """Adjust the plot.

        Parameters
        ----------
        bins : int
            The number of bins to use when plotting the distributions.
        distribution_scaling : float
            Scale the distribution plot in its y-direction by this amount.
        distribution_xline : float
            Place the distribution plot's x-axis at this point along the runway.
        runway_end : float
            Place the runway end at this point relative to the data points.
        runway_start : float
            Place the runway start at this point relative to the data points.
        runway_data_kwargs : dict | None
            Keyword arguments to give to the runway scatter plot.
        dist_data_kwargs : dict | None
            Keyword arguments to give to the distribution plot's data.
        dist_ctrl_kwargs : dict | None
            Keyword arguments to give to the distribution plot's control.
        """
        if runway_data_kwargs is None:
            _runway_data_kwargs = {
                "marker": "*",
                "c": "magenta",
                "s": 12,
                "zorder": 10,
            }
        else:
            _runway_data_kwargs = runway_data_kwargs
        if dist_data_kwargs is None:
            _dist_data_kwargs = {
                "marker": "o",
                "c": "magenta",
                "s": 3,
                "zorder": 5,
            }
        else:
            _dist_data_kwargs = dist_data_kwargs
        if dist_ctrl_kwargs is None:
            _dist_ctrl_kwargs = {
                "marker": "d",
                "c": "orange",
                "s": 3,
                "zorder": 5,
            }
        else:
            _dist_ctrl_kwargs = dist_ctrl_kwargs
        self.distribution_scaling = distribution_scaling
        self.distribution_xline = distribution_xline
        self.runway_end = runway_end
        self.runway_start = runway_start
        self.runway_data_kwargs = _runway_data_kwargs
        self.dist_data_kwargs = _dist_data_kwargs
        self.dist_ctrl_kwargs = _dist_ctrl_kwargs

    @staticmethod
    def dist_func_discrete_pdf(
        n_bins: int, values: NDArray[np.float64]
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Probability distribution function estimate (discrete)."""
        out = fppanalysis.distribution(values, n_bins, ccdf=False)
        return out[2], out[0]

    @staticmethod
    def dist_func_continuous_pdf(
        x: NDArray[np.float64], y: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Probability distribution function estimate (continuous)."""
        fit_diff = scipy.stats.norm.fit(y)
        return scipy.stats.norm.pdf(x, *fit_diff)

    @staticmethod
    def dist_func_discrete_cdf(
        n_bins: int, values: NDArray[np.float64]
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Cumulative distribution function estimate (discrete)."""
        out = fppanalysis.distribution(values, n_bins, ccdf=False)
        return out[2], out[1]

    @staticmethod
    def dist_func_continuous_cdf(
        x: NDArray[np.float64], y: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Cumulative distribution function estimate (discrete)."""
        fit_diff = scipy.stats.norm.fit(y)
        return scipy.stats.norm.cdf(x, *fit_diff)

    def set_dist_func(
        self,
        dist_func_discrete: Callable[
            [int, NDArray[np.float64]],
            tuple[NDArray[np.float64], NDArray[np.float64]],
        ],
        dist_func_continuous: Callable[
            [NDArray[np.float64], NDArray[np.float64]],
            NDArray[np.float64],
        ],
    ) -> None:
        """Specify a custom distribution function to use in the plot.

        Two functions are expected, one discrete and one continuous. See the two
        implementaitons for PDF and CDF as examples.

        Parameters
        ----------
        dist_func_discrete : Callable[[int, NDArray[np.float64]], tuple[NDArray[np.float64], NDArray[np.float64]]]
            A function that takes in the number of bins and the values to use.
        dist_func_continuous : Callable[[NDArray[np.float64], NDArray[np.float64]], NDArray[np.float64]]
            A function that takes in the x-axis to to use and the y-values to fit to.
        """
        self.dist_func_discrete = dist_func_discrete  # type: ignore[assignment]
        self.dist_func_continuous = dist_func_continuous  # type: ignore[assignment]

    def _plot(
        self,
        ax: mpl.axes.Axes,
    ) -> mpl.axes.Axes:
        """Create an airport-plot on the given axes object."""
        ctrl_basis = -1 * self.control
        ctrl_bins, ctrl_dist = self.dist_func_discrete(self.bins, ctrl_basis)
        diff_basis = self.arr1 - self.arr2
        diff_bins, diff_dist = self.dist_func_discrete(self.bins, diff_basis)
        xy_range = np.sum([self.arr2, self.arr1], axis=0).flatten()
        # xmy_range = np.diff([self.arr1, self.arr2], axis=0).flatten()
        xy_range_diff = abs(xy_range.max() - xy_range.min())
        # xmy_range_diff = abs(xmy_range.max() - xmy_range.min())
        shift_x = (
            (
                (self.runway_end - self.runway_start) * self.distribution_xline
                + self.runway_start
            )
            * xy_range_diff
            + xy_range.min()
        ) / 2
        lims = (
            (self.runway_start * xy_range_diff + xy_range.min()) / 2,
            ((self.runway_end - 1) * xy_range_diff + xy_range.max()) / 2,
        )
        std = self.control.std() / 2
        ax.annotate(
            "",
            xy=(lims[1], lims[1]),
            xytext=(lims[0], lims[0]),
            arrowprops={
                "shrinkA": 0,
                "shrinkB": 0,
                "arrowstyle": "->",
                "lw": 0.7,
                "color": "grey",
            },
        )
        ax.fill(
            [lims[0] - std, lims[1] - std, lims[1] + std, lims[0] + std],
            [lims[0] + std, lims[1] + std, lims[1] - std, lims[0] - std],
            "grey",
            alpha=0.3,
        )
        ax.fill(
            [
                lims[0] - 2 * std,
                lims[1] - 2 * std,
                lims[1] + 2 * std,
                lims[0] + 2 * std,
            ],
            [
                lims[0] + 2 * std,
                lims[1] + 2 * std,
                lims[1] - 2 * std,
                lims[0] - 2 * std,
            ],
            "grey",
            alpha=0.3,
        )
        dist_ax_start = 1.05 * max(diff_bins.max(), ctrl_bins.max()) / 2
        dist_ax_end = 1.30 * min(ctrl_bins.min(), diff_bins.min()) / 2
        ax.annotate(
            self.ax_labels[2],
            xy=(dist_ax_start + shift_x, -dist_ax_start + shift_x),
            xytext=(dist_ax_end + shift_x, -dist_ax_end + shift_x),
            arrowprops={
                "shrinkA": 0,
                "shrinkB": 0,
                "lw": 0.7,
                "relpos": (1, 0),
                "color": "grey",
                "arrowstyle": "<-",
            },
            c="grey",
            ha="right",
            va="bottom",
            size=6,
        )
        bins_diff_scaled = diff_bins / 2
        bins_diff_xskew, bins_diff_yskew = (
            bins_diff_scaled + shift_x,
            bins_diff_scaled - shift_x,
        )
        bins_ctrl_scaled = ctrl_bins / 2
        bins_ctrl_xskew, bins_ctrl_yskew = (
            bins_ctrl_scaled + shift_x,
            bins_ctrl_scaled - shift_x,
        )
        ax.scatter(
            bins_diff_xskew + diff_dist * self.distribution_scaling,
            diff_dist * self.distribution_scaling - bins_diff_yskew,
            label=self.labels[0],
            **self.dist_data_kwargs,  # type: ignore[arg-type]
        )
        ax.scatter(
            bins_ctrl_xskew + ctrl_dist * self.distribution_scaling,
            ctrl_dist * self.distribution_scaling - bins_ctrl_yskew,
            label=self.labels[1],
            **self.dist_ctrl_kwargs,  # type: ignore[arg-type]
        )
        norm_diff = self.dist_func_continuous(diff_bins, diff_basis)
        norm_ctrl = self.dist_func_continuous(ctrl_bins, ctrl_basis)
        ax.plot(
            bins_diff_xskew + norm_ctrl * self.distribution_scaling,
            norm_ctrl * self.distribution_scaling - bins_diff_yskew,
            c=self.dist_data_kwargs["c"],
        )
        ax.plot(
            bins_ctrl_xskew + norm_diff * self.distribution_scaling,
            norm_diff * self.distribution_scaling - bins_ctrl_yskew,
            c=self.dist_ctrl_kwargs["c"],
        )
        ax.scatter(
            self.arr1,
            self.arr2,
            label=self.labels[2],
            **self.runway_data_kwargs,  # type: ignore[arg-type]
        )
        ax.set_xlabel(self.ax_labels[0])
        ax.set_ylabel(self.ax_labels[1])
        ax.legend(loc="lower right")
        ylim_min = ax.get_ylim()[0]
        ylim_max = -1.70 * min(ctrl_bins.min(), diff_bins.min()) / 2 + shift_x
        ylim_max = max(ylim_max, ax.get_ylim()[1])
        ax.set_ylim((ylim_min, ylim_max + 0.05 * (ylim_max - ylim_min)))
        return ax


airport = Airport()
