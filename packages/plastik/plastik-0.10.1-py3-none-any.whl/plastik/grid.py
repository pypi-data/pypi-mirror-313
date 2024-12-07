"""Create and manipulate grids, similar to sub-figure layouts."""

import itertools
from typing import Any, Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing_extensions import Self


class FigureGrid:
    """Return a figure with axes appropriate for (rows, columns) sub-figures.

    Parameters
    ----------
    rows : int | None
        The number of rows in the figure
    columns : int | None
        The number of columns in the figure
    """

    def __init__(
        self: Self,
        rows: int | None = None,
        columns: int | None = None,
    ) -> None:
        self.rows = 1 if rows is None else rows
        self.columns = 1 if columns is None else columns
        self._labels: list[str] | None = None
        self._pos: tuple[float, float] = (-0.2, 0.95)
        self._share_axes: Literal["x", "y", "both"] | None = None
        self._columns_first: bool = False
        self._expand_top: float = 1.0

    def __call__(
        self: Self,
        rows: int,
        columns: int,
        using: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[Figure, list[Axes]]:
        """Create a figure with sub-figures in the given layout.

        Parameters
        ----------
        rows : int
            The number of rows in the figure.
        columns : int
            The number of columns in the figure.
        using : dict[str, Any] | None
            The properties to be used for the sub-figures. The keys are the keyword
            arguments used in the `using` method, see its signature for accepted values.
        **kwargs : Any
            Additional keyword arguments to be passed to `Axes.text`.

        Returns
        -------
        Figure
            A new matplotlib figure object.
        list[Axes]
            A list of all the axes objects owned by the figure.
        """
        self.rows, self.columns = rows, columns
        if using is not None:
            self.using(**using)
        return self.get_grid(**kwargs)

    def _calculate_figsize(self: Self) -> tuple[float, float]:
        """Calculate the figure size based on the number of rows and columns."""
        full_cols = 3.37 * self.columns
        squash_cols = 3.37 * self.columns - (self.columns - 1) * 3.37 * 0.25
        full_rows = 2.08277 * self.rows
        squash_rows = 2.08277 * self.rows - (self.rows - 1) * 2.08277 * 0.25
        match self._share_axes:
            case None:
                return full_rows, full_cols
            case "x":
                return squash_rows, full_cols
            case "y":
                return full_rows, squash_cols
            case "both":
                return squash_rows, squash_cols
            case _:
                raise ValueError(f"Unknown value for share_axes: {self._share_axes}")

    def _update_labels(self: Self) -> list[str]:
        labels = (
            [
                rf"$\mathrm{{({chr(97 + ell)})}}$"
                for ell in range(self.rows * self.columns)
            ]
            if not self._labels or len(self._labels) != int(self.rows * self.columns)
            else self._labels.copy()
        )
        return self._maybe_columns_first(labels)

    def _maybe_columns_first(
        self: Self, list_: list, *, transpose: bool = True
    ) -> list:
        if not self._columns_first:
            return list_
        if transpose:
            list_ = [
                list_[i * self.rows + j]
                for j in range(self.rows)
                for i in range(self.columns)
            ]
            return list_
        grid = [
            list_[i * self.columns : (i + 1) * self.columns] for i in range(self.rows)
        ]
        return [
            grid[row][col]
            for col, row in itertools.product(range(self.columns), range(self.rows))
        ]

    def using(  # noqa: PLR0913
        self: Self,
        *,
        labels: list[str] | None = None,
        pos: tuple[float, float] | None = None,
        share_axes: Literal["x", "y", "both"] | None = None,
        columns_first: bool | None = None,
        expand_top: float | None = None,
    ) -> Self:
        """Set text properties.

        The properties must be given as keyword arguments to take effect.

        Parameters
        ----------
        labels : list[str] | None
            The labels to be applied to each sub-figure. Defaults to (a), (b), (c), ...
        pos : tuple[float, float] | None
            The position in the sub-figure relative to the bottom-left corner. Default
            is `(-0.2, 0.95)`.
        share_axes : Literal["x", "y", "both"] | None
            Use a shared axis for the given direction. Default is `None`.
        columns_first : bool | None
            If the labels should be placed in a columns-first order. Default is `False`,
            meaning rows are numbered first.
        expand_top : float | None
            Make the figure higher by multiplying by `expand_top`. Note that the
            subfigures will remain the same. Useful for placing a common legend at the
            top of the figure.

        Returns
        -------
        Self
            The object itself.
        """
        self._labels = labels or self._labels
        self._pos = pos or self._pos
        self._share_axes = share_axes or self._share_axes
        self._columns_first = columns_first or self._columns_first
        self._expand_top = expand_top or self._expand_top
        return self

    def get_grid(
        self: Self,
        **kwargs: dict,
    ) -> tuple[Figure, list[Axes]]:
        """Return a figure with axes appropriate for (rows, columns) sub-figures.

        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments to be passed to Axes.text.

        Returns
        -------
        Figure
            The figure object
        list[Axes]
            A list of all the axes objects owned by the figure
        """
        full_height, full_width = self._calculate_figsize()
        fig = plt.figure(figsize=(full_width, full_height * self._expand_top))
        axes = []
        labels = self._update_labels()
        for r in range(self.rows):
            if self._share_axes in {"x", "both"}:
                rel_height = 0.75 + 0.25 / self.rows / self._expand_top
                height = 0.75 / self.rows / rel_height / self._expand_top
                bottom_pad = 0.2 / self.rows / rel_height / self._expand_top
                bottom = bottom_pad + height * (self.rows - 1 - r)
            else:
                bottom_pad = 0.2 / self.rows
                height = 0.75 / self.rows / self._expand_top
                bottom = bottom_pad + (self.rows - 1 - r) / self.rows / self._expand_top
            for c in range(self.columns):
                if self._share_axes in {"y", "both"}:
                    rel_width = 0.75 + 0.25 / self.columns
                    width = 0.75 / self.columns / rel_width
                    left_pad = 0.2 / self.columns / rel_width
                    left = left_pad + width * c
                else:
                    left_pad = 0.2 / self.columns
                    width = 0.75 / self.columns
                    left = left_pad + c / self.columns
                axes.append(fig.add_axes((left, bottom, width, height)))
                if self._share_axes in {"x", "both"} and r != self.rows - 1:
                    axes[-1].set_xticklabels([])
                if self._share_axes in {"y", "both"} and c != 0:
                    axes[-1].set_yticklabels([])
                axes[-1].text(
                    self._pos[0],
                    self._pos[1],
                    labels[self.columns * r + c],
                    transform=axes[-1].transAxes,
                    **kwargs,
                )
        axes = self._maybe_columns_first(axes, transpose=False)
        return fig, axes


figure_grid = FigureGrid()
