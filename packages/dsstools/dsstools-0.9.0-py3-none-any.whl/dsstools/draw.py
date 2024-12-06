# Copyright (C) 2024 dssTools Developers
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Module for drawing network images through method chaining."""

from __future__ import annotations

import json
import logging
import math
from collections import Counter
from copy import deepcopy
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

from . import mapping, processing
from .utils import _deprecate, NumpyEncoder
from .mapping import GenericMapping, fixed

draw_logger = logging.getLogger("draw_logger")


# TODO Upstream this
# The following function is distributed through NetworkX and contains
# adaptions by the following developers:
# David Seseke <david.seseke@uni-hamburg.de>
# Katherine Shay < katherine.shay@studium.uni-hamburg.de>
#
# The following license applies to this function:
# Copyright (C) 2004-2024, NetworkX Developers
# Aric Hagberg <hagberg@lanl.gov>
# Dan Schult <dschult@colgate.edu>
# Pieter Swart <swart@lanl.gov>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.

#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.

#   * Neither the name of the NetworkX Developers nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.


# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
def _draw_networkx_multiple_labels(
    G,
    pos,
    labels: dict,
    font_size=12,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    clip_on=True,
    hide_ticks=True,
):
    """Draw node labels on the graph G.

    Parameters
    ----------
    G : graph
        A networkx graph

    pos : dictionary
        A dictionary with nodes as keys and positions as values.
        Positions should be sequences of length 2.

    labels (dict): Node labels in a dictionary of text labels keyed by node.
        Node-keys in labels should appear as keys in `pos`.
        If needed use: `{n:lab for n,lab in labels.items() if n in pos}`

    font_size : int or array of ints (default=12)
        Font size for text labels

    font_color : color or array of colors (default='k' black)
        Font color string. Color can be string or rgb (or rgba) tuple of
        floats from 0-1.

    font_weight : string or array of strings (default='normal')
        Font weight

    font_family : string or array of strings (default='sans-serif')
        Font family

    alpha : float or array of floats or None (default=None)
        The text transparency

    bbox : Matplotlib bbox, (default is Matplotlib's ax.text default)
        Specify text box properties (e.g. shape, color etc.) for node labels.

    horizontalalignment : string (default='center')
        Horizontal alignment {'center', 'right', 'left'}

    verticalalignment : string (default='center')
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

    ax : Matplotlib Axes object, optional
        Draw the graph in the specified Matplotlib axes.

    clip_on : bool (default=True)
        Turn on clipping of node labels at axis boundaries

    Returns
    -------
    dict
        `dict` of labels keyed on the nodes

    Examples
    --------
    >>> G = nx.dodecahedral_graph()
    >>> labels = nx.draw_networkx_labels(G, pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    https://networkx.org/documentation/latest/auto_examples/index.html

    See Also
    --------
    draw
    draw_networkx
    draw_networkx_nodes
    draw_networkx_edges
    draw_networkx_edge_labels
    """
    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.gca()

    text_items = {}  # there is no text collection so we'll fake one
    for n, label in labels.items():
        (x, y) = pos[n]
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same
        t = ax.text(
            x,
            y,
            label,
            size=font_size[n],
            color=font_color[n],
            family=font_family[n],
            # TODO Make font_weight selectable
            weight=font_weight,
            alpha=alpha[n],
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            transform=ax.transData,
            bbox=bbox,
            clip_on=clip_on,
        )
        text_items[n] = t

    if hide_ticks:
        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False,
        )

    return text_items


def comfort_fixed(attribute: str | int | float | GenericMapping) -> GenericMapping:
    if isinstance(attribute, GenericMapping):
        return attribute
    else:
        return fixed(attribute)


def comfort_str_fixed(attribute: str | GenericMapping) -> GenericMapping:
    if isinstance(attribute, str) or isinstance(attribute, GenericMapping):
        return comfort_fixed(attribute)
    else:
        raise TypeError(
            f"'{type(attribute)}' is not of type 'GenericMapping' | str. To see what "
            f"to pass here, read the documentation on Mapping."
        )


def comfort_numeric_fixed(attribute: int | float | GenericMapping) -> GenericMapping:
    if isinstance(attribute, (float, int, GenericMapping)):
        return comfort_fixed(attribute)
    else:
        raise TypeError(
            f"'{type(attribute)}' is not of type 'GenericMapping' | int. To see what "
            f"to pass here, read the documentation on Mapping."
        )


class GraphElement:
    def set_colors(self, arg: GenericMapping | str):
        """Sets the colors of the displayed nodes.

        Args:
          arg: Colors to set. String values will be mapped onto all nodes.

        Returns:
          self
        """
        self.colors = comfort_fixed(arg)
        return self

    def set_sizes(self, arg: GenericMapping | int | float):
        """Sets size of labels for nodes as pt sizes.

        Args:
            arg: Font size for text labels
        Returns:
            self
        """

        self.sizes = comfort_numeric_fixed(arg)

        return self

    def set_alphas(self, arg: GenericMapping | float):
        """Sets alpha based on argument.

        Args:
            arg: The text transparency mapping as mapping.
        Returns:
            self
        """
        self.alphas = comfort_fixed(arg)
        return self

    def set_transparency(self, arg: GenericMapping | float):
        """Sets transparency based on argument.

        This is the same as `set_alphas()`. Alpha is the value for the transparency of a
        color.

        Args:
            arg: The text transparency mapping as mapping.
        Returns:
            self
        """
        return self.set_alphas(arg)


class Labels(GraphElement):
    def __init__(self):
        self.show_labels = False
        self.labels = []
        self.sizes = fixed(12)
        self.colors = fixed("black")
        self.alphas = fixed(1.0)
        self.font_families = fixed("DejaVu Sans")

    def set_labels(self, arg: dict[int, str] | dict[int, int]):
        """Sets labels for nodes based on arguments.

        Args:
           arg (dict): node identifier as the integer and the label as the string
        """
        self.show_labels = True
        self.labels = arg
        return self

    def set_font_families(self, arg: GenericMapping | str):
        """Sets font family for all labels if single font is passed,.

        Allows for multiple fonts to be set if an array of fonts is passed,
        allows for fonts to be individually set for labels based on the given
        node if a dictionary is passed.

        Args:
            arg: Font family
        """
        if isinstance(arg, str):
            if mpl.font_manager.findfont(arg, fallback_to_default=False) is None:
                raise ValueError("Font family not supported.")

        self.font_families = comfort_str_fixed(arg)
        return self


class Nodes(GraphElement):
    def __init__(self, labels=None):

        self.labels = labels

        self.positions = None
        self.sizes = fixed(50)
        self.colors = fixed("lightgrey")
        self.alphas = 1

        self.contour_colors = fixed("white")
        self.contour_sizes = fixed(0.5)

    def set_positions(self, pos: dict | list | Path | str):
        """Sets the node positions as a dict or list.

        When using a file, use `set_position_file()` instead.

        Args:
          pos: dict | list: Array of positions. Dicts should be keyed by node ID.

        Returns:
          self
        """
        if isinstance(pos, (Path, str)):
            filep = Path(pos)
            if filep.exists():
                self.positions = processing.Layouter().read_from_file(pos)
                return self
            raise FileNotFoundError("Position file was not found under the given path.")
        self.positions = pos
        return self

    def set_sizes(self, arg: GenericMapping | float | int):
        """Sets the sizes of the displayed nodes.

        Args:
          arg: Sizes to set. Scalar values will be mapped onto all nodes. String values
          will get mapped onto the corresponding data arrays or closeness values per
          node.

        Returns:
          self
        """
        argument = comfort_numeric_fixed(arg)
        if isinstance(argument, mapping.Sequential):
            self.sizes = argument.also(lambda x: math.sqrt(x))
        else:
            self.sizes = argument
        return self

    def set_contour_colors(self, arg: GenericMapping | str):
        """Sets the contour color of the displayed nodes.

        Contour means the outer border of a node.

        Args:
          arg: Colors to set. String values will be mapped onto all node contours.
            Additional options contain "node" and "edge" to automatically select the
            corresponding color.

        Returns:
          self
        """
        self.contour_colors = comfort_fixed(arg)
        return self

    def set_contour_sizes(self, arg: GenericMapping | float | int):
        """Sets the contour sizes of the displayed nodes.

        Contour means the outer border of a node.

        Args:
          arg: Sizes to set. Integer values will be mapped onto all node contours.
            String values will get mapped onto the corresponding data arrays or closeness
            values per node.

        Returns:
          self
        """
        self.contour_sizes = comfort_numeric_fixed(arg)
        return self


class Edges(GraphElement):
    def __init__(self, labels=None):
        self.labels = labels

        self.sizes = fixed(0.5)
        self.colors = fixed("lightgrey")
        self.arrow_size = 2


class Description:
    """Class containing description drawing preferences."""

    def __init__(self):
        self.text = ""
        self.alpha = 0.5
        self.size = 8

    def set_text(self, text: str):
        """Sets the description setting.

        Args:
          text: Text to set as description

        Returns:
        """
        self.text = text
        return self


class ImageGenerator:
    """Base class for setting up image generation."""

    # NOTE Proposal: Move all the default settings from settings.py to this init
    # TO-DO set graph not param
    def __init__(self, graph):
        self.graph = graph
        self.axis = None
        self._fig = None
        self.img_dir = Path(".")
        self.continous_cmap = mpl.colormaps["viridis"]
        self.qualitative_cmap = mpl.colormaps["tab10"]

        self.description = Description()

        self.nodes = Nodes(Labels())
        self.edges = Edges()

        # Legend/other
        self._handles = {}
        self.show_legend = False
        self.value_not_assigned = "keine Angabe"
        self.axis_legend_loc = 1

        # Canvas
        self.dpi = 200
        self.canvas_height = 10
        self.canvas_width = 10
        self.axlimit = 1.05

    def _check_positions(self):
        if self.nodes.positions is not None:
            return self.nodes.positions
        raise ValueError(
            "Node(s) have no position data. Try setting positions using nodes.set_positions() or use processing.Layouter to create a graph"
        )

    def change_graph(self, graph):
        """Sets the graph attribute.

        Args:
          graph: A NetworkX graph object.

        Returns:
          self
        """
        self.graph = graph
        return self

    def set_legend(self, legend=True):
        """Sets the legend setting.

        Args:
          legend: (default = True) Whether to show the legend.

        Returns:
          self
        """
        self.show_legend = legend
        return self

    def set_axis(self, axis):
        """Sets an existing matplotlib axis object for the ImageGenerator
        object.

        Args:
          axis: Matplotlib axis

        Returns:
          self
        """
        self.axis = axis
        return self

    def _map_color_to_edges(self, attribute: str) -> dict:
        """Map color onto edges.

        Args:
          graph(nx.Graph): Graph containing edges.
          attribute(str): The attribute to map colors to.
          attribute: str:

        Returns:
          : Dict of edge tuples and the corresponding color.
        """
        colors = nx.get_node_attributes(self.graph, attribute).values()
        edge_colors = {}
        sorted_colors = dict(sorted(Counter(colors).items(), key=lambda item: item[1]))
        node_colors_d = dict(zip(self.graph.nodes, colors))
        for edge in self.graph.edges:
            node_start = sorted_colors[node_colors_d[edge[0]]]
            node_end = sorted_colors[node_colors_d[edge[1]]]
            if node_start >= node_end:
                edge_colors[edge] = node_colors_d[edge[1]]
            else:
                edge_colors[edge] = node_colors_d[edge[0]]
        return edge_colors

    def _setup_canvas(self):
        """Prepare the correct canvas and set to attributes."""
        if not self.axis:
            self._fig, self.axis = plt.subplots(
                1, 1, figsize=(self.canvas_width, self.canvas_height)
            )
            self._fig.subplots_adjust(
                left=0, bottom=0, right=1, top=1, wspace=0, hspace=0
            )
            # Use slightly increased limits to prevent clipping
            self.axis.set_xlim([-self.axlimit, self.axlimit])
            self.axis.set_ylim([-self.axlimit, self.axlimit])
            self.axis.axis("off")
        elif not self._fig:
            self._fig = self.axis.get_figure()

    def draw_nodes(self):
        """Draw nodes according to the settings."""
        self._check_setup()
        self._setup_canvas()
        node_positions = self._check_positions()

        node_sizes = self.nodes.sizes.get(self.graph.nodes(data=True), self.graph)
        node_colors = self.nodes.colors.get(self.graph.nodes(data=True), self.graph)
        node_contour_sizes = self.nodes.contour_sizes.get(
            self.graph.nodes(data=True), self.graph
        )
        node_contour_colors = self.nodes.contour_colors.get(
            self.graph.nodes(data=True), self.graph
        )

        nx.draw_networkx_nodes(
            self.graph,
            pos=node_positions,
            node_size=list(node_sizes.values()),  # type: ignore
            node_color=list(node_colors.values()),  # type: ignore
            linewidths=list(node_contour_sizes.values()),
            edgecolors=list(node_contour_colors.values()),
            ax=self.axis,
        )
        return self

    def draw_edges(self):
        """Draw edges according to the settings."""
        self._check_setup()
        self._setup_canvas()

        node_positions = self._check_positions()

        node_sizes = self.nodes.sizes.get(self.graph.nodes(data=True), self.graph)
        edge_colors = self.edges.colors.get(self.graph.edges, self.graph)
        edge_sizes = self.edges.sizes.get(self.graph.edges, self.graph)

        nx.draw_networkx_edges(
            self.graph,
            pos=node_positions,
            edge_color=list(edge_colors.values()),
            width=list(edge_sizes.values()),
            arrows=self.edges.arrow_size > 0,
            arrowsize=self.edges.arrow_size,
            ax=self.axis,
            node_size=list(node_sizes.values()),
            alpha=1,
        )
        return self

    def draw_labels(self):
        """Draws labels based on values."""
        self._check_setup()
        self._setup_canvas()

        if not self.nodes.labels.labels:
            labels = {n: n for n in self.graph.nodes}
            self.nodes.labels.set_labels(labels)

        # self._check_font_family()

        node_positions = self._check_positions()

        labels_size = self.nodes.labels.sizes.get(
            self.graph.nodes(data=True), self.graph
        )
        labels_color = self.nodes.labels.colors.get(
            self.graph.nodes(data=True), self.graph
        )
        labels_font_family = self.nodes.labels.font_families.get(
            self.graph.nodes(data=True), self.graph
        )
        labels_alpha = self.nodes.labels.alphas.get(
            self.graph.nodes(data=True), self.graph
        )

        _draw_networkx_multiple_labels(
            self.graph,
            labels=self.nodes.labels.labels,
            pos=node_positions,
            font_size=labels_size,
            font_color=labels_color,
            font_family=labels_font_family,
            alpha=labels_alpha,
            ax=self.axis,
        )

        return self

    def draw_description(self):
        """Draw description below the image according to the settings."""
        self._check_setup()
        self._setup_canvas()
        if self.description.text and self.axis is not None:
            self.axis.text(
                0.95,
                0.1,
                self.description.text,
                size=self.description.size,
                ha="right",
                transform=self.axis.transAxes,
                alpha=self.description.alpha,
            )
        return self

    # TODO This is a placeholder until the proper handling of color legends is decided upon.
    def draw_legend(self):
        """Not yet implemented."""
        raise NotImplementedError("This feature is yet to be implemented.")
        # # TODO Problem: There can be both the need for a color bar (even two) as
        # # well as a regular legend. Accordingly the space necessary for the image
        # # needs to be extended.
        # # Problem discussed here: https://github.com/matplotlib/matplotlib/issues/15010
        # # Make an outside of image legend?
        # # Use this:
        # https://matplotlib.org/stable/api/toolkits/axes_grid1.html#module-mpl_toolkits.axes_grid1
        # handles = []
        # a_lcolor = "_node_color_legend"  # Exctracted from settings
        # a_lccolor  # was never in settings.py. Can't find it here either
        # a_lecolor = "_edge_color_legend"  # Extracted from settings
        # for lg in [a_lcolor, a_lccolor, a_lecolor]:
        #     if nc := graph.graph.get(lg):
        #         if isinstance(nc, list):
        #             handles += nc
        #         elif isinstance(nc, matplotlib.cm.ScalarMappable):
        #             # TODO I'm very unsure how to handle this -> Maybe draw an
        #             # additional image for the scalar color map?
        #             raise NotImplementedError()
        #         else:
        #             raise NotImplementedError()
        # if handles:
        #     ax.legend(handles=handles, loc=settings.axis_legend_loc, numpoints=1)

    def draw(self):
        self.draw_edges().draw_nodes()
        self.draw_labels()  # Must not check for nodes.labels: Default will be set later
        if self.description.text:
            self.draw_description()
        if self.show_legend:
            self.draw_legend()
        return self

    def write_file(self, path: str | Path):
        """Write file to disk on the given path.

        Will also close the internal figure object.

        Args:
          path: str | Path: Path to write the file to.

        Returns:
          self
        """
        path = Path(path)
        filepath, file_format = ensure_file_format(
            path, path.suffix, default_format=".svg"
        )

        self._fig.savefig(filepath, format=file_format, dpi=self.dpi)
        draw_logger.info(f"Written graph image to {filepath}.")
        plt.close(self._fig)
        return self

    def deepcopy(self):
        """Create deep copy of the object.

        This is the same as calling copy.deepcopy() on the object
        """
        return deepcopy(self)

    def _check_setup(self):
        """Check if the setup is sufficient for drawing."""
        errors = []
        if self.graph is None:
            errors.append("Please set a graph.")
        # TODO maybe call self.check_positions() instead of in draw calls

        if not (self.nodes.positions):
            errors.append("Positions are not set.")
        elif set(self.graph.nodes) - set(self.nodes.positions.keys()):
            errors.append("Positions are not the same size as node list.")

        if len(errors) > 0:
            [draw_logger.error(e) for e in errors]
            raise ValueError("There are missing values in your draw setup.")

    def write_json(self, path: str | Path) -> "ImageGenerator":
        """Writes the graph data to a json file following nx.node_link_data
        format.

        Args:
            path: saving location and name for the json-file

        Returns:
            self
        """
        # TODO: Validate path with new helper method

        # Validates that a position attribute is set or raises an error
        node_positions = self._check_positions()
        # Ensure we do not change the original graph with our new attributes
        export_graph = deepcopy(self.graph)

        # Adding 'x' and 'y' as attributes for nodes
        node_sizes = self.nodes.sizes.get(export_graph.nodes(data=True), export_graph)
        node_colors = self.nodes.colors.get(export_graph.nodes(data=True), export_graph)
        edge_colors = self.edges.colors.get(export_graph.edges(data=True), export_graph)
        edge_sizes = self.edges.sizes.get(export_graph.edges(data=True), export_graph)

        # Sets the attributes explicitly as x and y coordinates for all nodes
        for node in export_graph.nodes:
            n = export_graph.nodes[node]
            n["x"] = node_positions[node][0]
            n["y"] = node_positions[node][1]
            n["nodeColor"] = node_colors[node]
            n["nodeSize"] = node_sizes[node]
        # # FIXME This is breaking due to an incorrect get function.
        # for edge in export_graph.edges:
        #     e = export_graph.edges[edge]
        #     e["edgeColor"] = edge_colors[edge]
        #     e["edgeSize"] = edge_sizes[edge]

        # Output to JSON format
        data = nx.node_link_data(export_graph)
        with open(path, "w") as file:
            # The Encoder ensure that np.ndarrays can be saved (as lists)
            json.dump(data, file, indent=4, cls=NumpyEncoder)

        return self


@_deprecate("Use ImageCollection.create_multiple_in_one() instead.")
def draw_network_slices(
    igs: list[ImageGenerator],
    fig: mpl.figure.Figure,
    fpath: Path | None = None,
    *,
    dpi: int = 200,
):
    if len(igs) != len(fig.axes):
        raise ValueError("List of graphs and axes in figure are not the same length.")

    for ig, ax in zip(igs, fig.axes):
        ig.set_axis(ax).draw()
        ax.set_axis_off()

    if fpath:
        fpath, file_format = ensure_file_format(
            fpath, fpath.suffix, default_format=".svg"
        )
        fig.savefig(fpath, format=file_format, dpi=dpi)

    return fig


def ensure_file_format(
    path: str | Path, user_saving_format: str | None, *, default_format: str
) -> tuple[Path, str]:
    """Ensures that the provided path has a saving format.

    Args:
        path: the path that needs to be validated
        user_saving_format: the saving format provided by the user
        default_format: the format a programmer can set that will be used as default, if
            no format was provided at all

    Returns:
        the filepath and format (without leading dot) as an 2-Tuple
    """
    # Ensures Path-operations
    if isinstance(path, str):
        path = Path(path)

    # If no format was specified
    if not path.suffix and not user_saving_format:
        # This should be replaced by a logger warning
        print(
            f"No saving format was provided in the 'save_path' or directly "
            f"via 'saving_format'. '{default_format}' was used as default"
        )
        user_saving_format = default_format

    # 'user_saving_format' is always valued higher than path suffix
    if user_saving_format:
        # If user forgot the leading dot
        if not user_saving_format.startswith("."):
            user_saving_format = "." + user_saving_format
        path = path.with_suffix(user_saving_format)

    cleaned_suffix = path.suffix.strip(".")
    return path, cleaned_suffix
