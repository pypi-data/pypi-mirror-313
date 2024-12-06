"""Single-Shot plotting functionality.

This module provides plotting capabilities for single-shot quantum measurements,
including scatter plots and line plots with customizable styling.
"""

from typing import Optional, Dict, Any
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import ArrayLike

from qubit_measurement_analysis.visualization.base_plotter import (
    BasicShotPlotter as bsp,
)
from qubit_measurement_analysis.visualization.utils import _get_current_kwargs


class SingleShotPlotter:
    """Plotter class for visualizing single-shot quantum measurements.

    This class provides methods for creating scatter plots and line plots
    of single-shot measurement data, with support for customizable styling
    and automatic qubit state labeling.

    Attributes:
        children: The SingleShot instance to plot
    """

    def __init__(self, children: Any) -> None:
        """Initialize the plotter.

        Args:
            children: SingleShot instance containing the data to plot
        """
        self.children = children

    def _prepare_plot(
        self, ax: Optional[Axes] = None, **kwargs: Any
    ) -> tuple[Axes, Dict[str, Any]]:
        """Prepare plotting environment.

        Args:
            ax: Matplotlib axes to plot on
            **kwargs: Additional keyword arguments for plotting

        Returns:
            Tuple of (matplotlib axes, copied kwargs dict)
        """
        if ax is None:
            _, ax = plt.subplots()
        return ax, kwargs.copy()

    def scatter(self, ax: Optional[Axes] = None, **kwargs: Any) -> Axes:
        """Create a scatter plot of the measurement data.

        Creates a scatter plot where each point represents a measurement value,
        with optional automatic state labeling for demodulated data.

        Args:
            ax: Matplotlib axes to plot on. If None, creates new figure
            **kwargs: Additional keyword arguments passed to scatter:
                - marker: Custom marker style
                - label: Custom label for legend
                - color: Point color
                - alpha: Point transparency
                - s: Point size
                - etc.

        Returns:
            The matplotlib axes containing the plot

        Example:
            >>> plotter.scatter(color='blue', alpha=0.5)
        """
        ax, kwargs_ = self._prepare_plot(ax, **kwargs)

        for reg_idx, qubit in enumerate(self.children.qubits):
            # Set marker to qubit state if demodulated and no custom marker
            if kwargs.get("marker") is None:
                if self.children.is_demodulated:
                    marker = f"${self.children.classes[reg_idx]}$"
                    kwargs_.update({"marker": marker})

            # Set qubit index as label if no custom label
            if kwargs.get("label") is None:
                if self.children.is_demodulated:
                    kwargs_.update({"label": str(qubit)})

            current_kwargs = _get_current_kwargs(kwargs_, reg_idx)
            bsp.scatter_matplotlib(
                ax,
                self.children.value[reg_idx, :],
                **current_kwargs,
            )

            if not self.children.is_demodulated:
                break

        return ax

    def plot(
        self, ax: Optional[Axes] = None, x: Optional[ArrayLike] = None, **kwargs: Any
    ) -> Axes:
        """Create a line plot of the measurement data.

        Creates a line plot showing the real and imaginary components
        of the measurement values over time or custom x-coordinates.

        Args:
            ax: Matplotlib axes to plot on. If None, creates new figure
            x: Optional x-coordinates for the plot
            **kwargs: Additional keyword arguments passed to plot:
                - label: Custom label(s) for legend
                - color: Line color(s)
                - linestyle: Line style
                - linewidth: Line width
                - marker: Point marker
                - etc.

        Returns:
            The matplotlib axes containing the plot

        Example:
            >>> plotter.plot(linestyle='--', marker='o')
        """
        ax, kwargs_ = self._prepare_plot(ax, **kwargs)

        for reg_idx, qubit in enumerate(self.children.qubits):
            # Set default labels for real and imaginary components
            if kwargs.get("label") is None:
                if self.children.is_demodulated:
                    kwargs_.update({"label": ([f"$I$({qubit})", f"$Q$({qubit})"])})
                current_kwargs = kwargs_.copy()
            else:
                current_kwargs = _get_current_kwargs(kwargs_, reg_idx)

            bsp.plot_matplotlib(
                ax,
                self.children.value[reg_idx, :],
                x=x,
                **current_kwargs,
            )

            if not self.children.is_demodulated:
                break

        return ax
