"""Shot Collection plotting functionality.

This module provides visualization capabilities for collections of quantum measurement shots,
including scatter plots and histogram plots with customizable styling.
"""

from typing import Optional, Dict, Any, List, Tuple, Union
from matplotlib import pyplot as plt
from matplotlib.axes import Axes

from qubit_measurement_analysis.visualization.base_plotter import (
    BasicShotPlotter as bsp,
)
from qubit_measurement_analysis.visualization.utils import _get_current_kwargs


class CollectionPlotter:
    """Plotter class for visualizing collections of quantum measurement shots.

    This class provides methods for creating scatter plots and histograms
    of shot collections, with support for customizable styling and automatic
    state labeling.

    Attributes:
        children: The ShotCollection instance to plot
    """

    def __init__(self, children: Any) -> None:
        """Initialize the plotter.

        Args:
            children: ShotCollection instance containing the data to plot
        """
        self.children = children

    def _prepare_plot(self, ax: Optional[Axes] = None) -> Axes:
        """Prepare plotting environment.

        Args:
            ax: Matplotlib axes to plot on

        Returns:
            Matplotlib axes for plotting
        """
        if ax is None:
            _, ax = plt.subplots()
        return ax

    def _prepare_histogram_data(
        self,
        counts: Dict[str, Union[int, float]],
        correct_key: Optional[str] = None,
        correct_color: Optional[str] = None,
        default_color: str = "tab:blue",
    ) -> Tuple[List[str], List[Union[int, float]], List[str]]:
        """Prepare data for histogram plotting.

        Args:
            counts: Dictionary of counts or probabilities
            correct_key: Key to highlight
            correct_color: Color for highlighted key
            default_color: Default bar color

        Returns:
            Tuple of (labels, values, colors)
        """
        # Sort items for consistent display
        sorted_items = sorted(counts.items())
        labels, values = zip(*sorted_items)

        # Prepare colors list
        colors = [default_color] * len(labels)
        if correct_key in labels:
            index = labels.index(correct_key)
            colors[index] = correct_color

        return labels, values, colors

    def scatter(self, ax: Optional[Axes] = None, **kwargs: Any) -> Axes:
        """Create a scatter plot of the measurement data.

        Creates a scatter plot where each point represents a measurement value,
        with automatic grouping by qubit and state.

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
        ax = self._prepare_plot(ax)

        for i, qubit in enumerate(self.children.qubits):
            for class_ in self.children.unique_classes_by_qubit(qubit):
                collection = self.children.filter_by_qubits_classes({qubit: class_})
                current_kwargs = _get_current_kwargs(kwargs, i)

                # Set marker to state if demodulated and no custom marker
                if current_kwargs.get("marker") is None:
                    if self.children.is_demodulated:
                        marker = f"${class_}$"
                        current_kwargs["marker"] = marker

                # Set qubit index as label if no custom label
                if current_kwargs.get("label") is None:
                    if self.children.is_demodulated:
                        current_kwargs["label"] = str(qubit)

                bsp.scatter_matplotlib(
                    ax,
                    collection.all_values[:, i, :],
                    **current_kwargs,
                )
            if not self.children.is_demodulated:
                break
        return ax

    def plot_hist(
        self,
        ax: Optional[Axes] = None,
        correct_key: Optional[str] = None,
        correct_color: Optional[str] = None,
        default_color: str = "tab:blue",
    ) -> Axes:
        """Create a histogram of shot counts.

        Creates a bar plot showing the count of shots for each state.

        Args:
            ax: Matplotlib axes to plot on. If None, creates new figure
            correct_key: State to highlight
            correct_color: Color for highlighted state
            default_color: Default bar color

        Returns:
            The matplotlib axes containing the plot

        Example:
            >>> plotter.plot_hist(correct_key='0', correct_color='green')
        """
        ax = self._prepare_plot(ax)
        labels, counts, colors = self._prepare_histogram_data(
            self.children.counts, correct_key, correct_color, default_color
        )

        ax.bar(labels, counts, color=colors)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right")
        return ax

    def plot_hist_proba(
        self,
        ax: Optional[Axes] = None,
        correct_key: Optional[str] = None,
        correct_color: Optional[str] = None,
        default_color: str = "tab:blue",
    ) -> Axes:
        """Create a histogram of shot probabilities.

        Creates a bar plot showing the probability distribution of states.

        Args:
            ax: Matplotlib axes to plot on. If None, creates new figure
            correct_key: State to highlight
            correct_color: Color for highlighted state
            default_color: Default bar color

        Returns:
            The matplotlib axes containing the plot

        Example:
            >>> plotter.plot_hist_proba(correct_key='0', correct_color='green')
        """
        ax = self._prepare_plot(ax)
        labels, probas, colors = self._prepare_histogram_data(
            self.children.counts_proba, correct_key, correct_color, default_color
        )

        ax.bar(labels, probas, color=colors)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right")
        return ax
