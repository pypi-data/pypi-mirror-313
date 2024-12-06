# Copyright (C) 2024 dssTools Developers
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
""""""

from __future__ import annotations

import json
import logging as lg
import random
from pathlib import Path
from typing import Union

import networkx as nx
import numpy as np

from .utils import NumpyEncoder, _deprecate


class Layouter:

    @staticmethod
    @_deprecate("Please use `Layouter`, `GraphvizLayouter` or `KamadaKawaiLayouter` directly instead.")
    def select(name: str = "") -> "Layouter":
        try:
            return next(
                layouter
                for layouter in Layouter.__subclasses__()
                if layouter.name() == name
            )()
        except StopIteration:
            return Layouter()

    @staticmethod
    def name() -> str:
            return "spring"

    def create_layout(self, graph: nx.Graph, seed=None, pos=None, **kwargs) -> None:
        """Create position dictionary according to set layout engine. Default
        layout is Spring.

        Args:
           graph (nx.Graph):  Graph object
           seed (int): Set a default seed (default None)
           pos: Pre-populated positions


        Returns:
            Dictionary of node and positions.
        """
        if seed is None:
            random.seed()
            seed = random.randrange(100000)

        lg.info(f"Using seed {seed} for generating positions.")

        # This produces ndarrays which are not JSON serializable so we convert them to lists
        return nx.spring_layout(graph, pos=pos, seed=seed, **kwargs)

    def read_or_create_layout(
        self,
        filepath: Union[str, Path],
        graph: nx.Graph,
        seed: int,
        overwrite=False,
        **kwargs,
    ) -> dict:
        """Read positions from file. If non-existant create pos and write to
        file.

        Args:
            filename (Union[str,Path]): Filename to read positions from
            graph (Graph): Graph object to update
            overwrite (bool): Overwrite existing file (default False)

        Returns:
            Dictionary of positions per Node. Will return an empty dict if creation
            failed.
        """

        path = Path(filepath)
        if path.is_file() and not overwrite:
            return self.read_from_file(filepath)
        if path.is_dir():
            raise ValueError("Provide a path for a filename, not a directory.")
        positions = self.create_layout(graph, seed=seed, **kwargs)
        self.write_to_file(positions, filepath)
        return positions if positions is not None else dict()

    def write_to_file(self, positions, path):
        with open(path, "w", encoding="UTF-8") as file:
            lg.info(f"Writing positions to '{path}'.")
            file.write(json.dumps(positions, cls=NumpyEncoder))

    @_deprecate("Please use `read_or_create_layout()` instead.")
    def update_positions(self, *args, **kwargs):
        return self.read_or_create_layout(*args, **kwargs)

    def read_from_graph(self, graph: nx.Graph, pos_name: tuple[str, str] = ("x", "y")):
        """Read positions from node attributes in the graph.

        This is relevant when importing from Pajek or GEXF files where the positions are
        already set with another tool. Imported values are normalized onto [-1,1] in all
        directions.

        Args:
            graph (nx.Graph): Graph object including the node attributes.
            pos_name (tuple): Node attribute names to look for. These depend on the
                              imported file format.

        Returns:
            Dictionary of positions per Node.
        """
        nodes_x = nx.get_node_attributes(graph, pos_name[0])
        nodes_y = nx.get_node_attributes(graph, pos_name[1])
        positions = {}

        # I am really sorry for this
        for (node, x), y in zip(nodes_x.items(), nodes_y.values()):
            positions[node] = [ x, y ]

        return {key: tuple(value) for key, value in nx.rescale_layout_dict(positions).items()}

    @_deprecate("Use `read_from_file` instead.")
    def read_positions(self, *args, **kwargs):
        return self.read_from_file(*args, **kwargs)

    def read_from_file(self, filename: Union[str, Path], **kwargs) -> dict:
        """Reads position from JSON file under filepath.

        The following structure for the JSON is expected, where each key contains an
        array of length 2 containing the coordinates. Coordinates should be in the range
        [-1,1]:

        ```json
        {
            "domain1": [-0.1467271130230262, 0.25512246449304427],
            "domain2": [-0.3683594304205127, 0.34942480334119136],
        }
        ```

        This structure is generated through `dsstools.Layouter().write_to_file()`.

        Args:
           filename (Union[str.Path]): Path to file to be read.
           graph (nx.Graph):

        Returns:
            Dictionary of nodes and positions.
        """
        path = Path(filename)
        if path.is_file():
            lg.info(f"Read positions from '{path}'.")
            with open(path, "r", encoding="UTF-8") as file:
                pos = json.load(file)
            # We need to convert back from lists to ndarray to maintain
            # compatibility with classic networkx
            ndarray_pos = {}
            for key in pos.keys():
                ndarray_pos[key] = np.asarray(pos[key])
            return ndarray_pos

        raise ValueError(f"Given file under {filename} does not exist.")

    # NX kwargs -> pos for initial positions


class GraphvizLayouter(Layouter):
    @staticmethod
    def name() -> str:
        return "graphviz"

    def create_layout(
        self, graph: nx.Graph, seed: int = -1, prog="fdp", additional_args=""
    ) -> dict:
        if seed < 0:
            random.seed()
            seed = random.randrange(100000)

        lg.info(f"Using seed {seed} for generating positions.")
        dot_args = f"-Gstart={seed} -Nshape=circle " + additional_args

        positions = nx.nx_agraph.graphviz_layout(graph, prog=prog, args=dot_args)
        return nx.rescale_layout_dict(positions)


class KamadaKawaiLayouter(Layouter):
    @staticmethod
    def name() -> str:
        return "kamada-kawai"

    def create_layout(self, graph: nx.Graph, seed=None, **kwargs) -> dict:
        lg.info("No seed for generating positions, so always save your layout.")
        if seed is not None:
            lg.info("Seed value for Kamada-Kawai layout is ignored.")

        return nx.kamada_kawai_layout(graph, **kwargs)


@_deprecate("Please use the native function `nx.betweenness_centrality()` instead")
def calculate_betweenness_centrality(graph: nx.Graph,
                                     name="_betweenness",
                                     **kwargs):
    """Updates the nodes in the graph with betweenness centrality.

    Args:
       graph: nx.Graph The graph to calculate on.
       name (str): Name of the centrality type.
       **kwargs: All arguments passed onto nx.betweenness_centrality (see
           https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html#betweenness-centrality)

    Returns:
       Graph including the closeness centrality.
    """
    centr = nx.betweenness_centrality(graph, **kwargs)
    nx.set_node_attributes(graph, centr, name=name)


@_deprecate("Please use the native function `nx.closeness_centrality()` instead")
def calculate_closeness_centrality(graph: nx.Graph,
                                   name: str = "_closeness",
                                   **kwargs):
    """Updates the nodes in the graph with closeness centrality.

    Args:
       graph: nx.Graph The graph to calculate on.
       name (str): Name of the centrality type.
       **kwargs: All arguments passed onto nx.closeness_centrality (see
           https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.closeness_centrality.html#closeness-centrality)

    Returns:
       Graph including the betweenness centrality.
    """
    centr = nx.closeness_centrality(graph, **kwargs)
    nx.set_node_attributes(graph, centr, name=name)
