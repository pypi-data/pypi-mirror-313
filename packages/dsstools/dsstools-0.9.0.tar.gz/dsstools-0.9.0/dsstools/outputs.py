# Necessary for Literal | None in export_overview_as()
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
from warnings import warn

import pandas as pd
import networkx as nx


@dataclass
class GraphDescriptor:
    """This class provides a dataframe (~table) view of the given graph.

    Every metric you add is its own column and every node its own row. It allows you
    to add custom metrics for more detailed analysis and save the dataframe as either
    csv or xlsx document.

    The naming hierarchy is as follows:
        - if activated, default metrics are always set first
        - if a custom metric is equal to a default metric, the values will be replaced
        - if a node attribute name is equal to regular or custom metric in df, the node
          attribute will have the number of duplicates as suffix
        - if two nodes have the same attribute, the attribute will be considered equal
          and their individual values will be in the same column

    Args:
        graph (nx.Graph): The graph you want to save/analyse
        include_defaults (bool): The class adds betweenness, degree and centrality as
            default metrics for all nodes. You can deactivate this behaviour by setting
            this to False (default True)
        round_floats_to (int): The class rounds every float down to 4 decimal points by
            default. This guarantees that cells won't grow to big, making it hard to
            analyse the data. Increase this value for more detailed

    """
    graph: nx.Graph
    include_defaults: bool = True
    round_floats_to: int = 4

    dataframe: pd.DataFrame = field(init=False)

    custom_calculations: dict[str, pd.Series] = field(init=False, default_factory=dict)

    def __post_init__(self):
        # Calculate metrics after initialization
        self.default_metrics = {
            "Betweenness": nx.betweenness_centrality(self.graph),
            "Degree": dict(self.graph.degree()),
            "Centrality": nx.degree_centrality(self.graph)
        }

    def get_dataframe(self) -> pd.DataFrame:
        if not hasattr(self, "dataframe"):
            self.__create_dataframe()
        return self.dataframe

    def add_custom_metrics(self,
                           custom_metrics: dict[str, callable]
                           ) -> 'GraphDescriptor':
        """Allows you to add custom graph metrics by passing a dictionary
        of metric names and functions that operate on the graph.

        Custom metrics will override default metrics if they are named the same.

        Examples:
            ```python
            def calculate_clustering(graph):
                return nx.clustering(graph)

            # Note how some values must be wrapped in a dictionary first,
            # else pandas will read them as NaN
            def calculate_shortest_path_length(graph):
                return dict(nx.shortest_path_length(graph))

            custom_metrics = {
                'Clustering': calculate_clustering,
                'Shortest path length': calculate_shortest_path_length,
                'Closeness': lambda graph: nx.closeness_centrality(graph)
            }

            GraphDescriptor(graph=mygraph).add_custom_metrics(custom_metrics)
            ```

        Args:
            custom_metrics (dict[str, callable]): A dictionary where keys are metric
                names and values are functions accepting a NetworkX graph and return a
                dictionary of node-based metric values (otherwise values in dataframe
                might be NaN).

        Returns:
            self
        """
        for metric_name, metric_func in custom_metrics.items():
            try:
                # Execute the function and store the result
                metric_result = metric_func(self.graph)

                # Store the result in dictionary to add them later
                self.custom_calculations[metric_name] = pd.Series(metric_result)

            except Exception as e:
                print(f"Error calculating metric {metric_name}: {e}")

        # Always recalculate Dataframe, if new metrics are added
        self.__create_dataframe()

        return self

    def __create_dataframe(self) -> None:
        """Creates a dataframe view of a graph where every Node is its own row (index)
        and every attribute its own column.

        If not all Nodes have the same attributes, 'None' will be set as placeholder
        value.
        """
        # First creation if the dataframe doesn't exist yet
        if not hasattr(self, "dataframe"):
            self.dataframe = pd.DataFrame(index=self.graph.nodes())

        # Adding fix calculated values (default metrics)
        if self.include_defaults:
            for metric_name, metric_result in self.default_metrics.items():
                self.dataframe[metric_name] = pd.Series(metric_result)

        # Adding custom values after defaults if available (custom metrics)
        if self.custom_calculations:
            # Metric names are unique by the nature of a dictionary
            for metric_name, metric_results in self.custom_calculations.items():
                self.dataframe[metric_name] = metric_results

        # Adding node attributes dynamically
        for node, data in self.graph.nodes(data=True):
            for key, value in data.items():
                col_name = self.__ensure_uniqueness(key)
                self.dataframe.at[node, col_name] = value

        # Rounding float columns (if needed) to the specified decimal places
        self.dataframe = self.dataframe.map(
            lambda x: round(x, self.round_floats_to) if isinstance(x, float) else x
        )

    def __ensure_uniqueness(self, col_name: str) -> str:
        """Ensures that no node attribute overrides a metric column.

        Warns the user, if an attribute is named the same as a metric.

        Args:
            col_name: Essentially the node attribute that needs to be checked.

        Returns:
            A unique name for the attribute.
        """
        counter = 0
        new_name = col_name
        # Is there a case where this can be >1? customs override defaults and customs
        # are unique. If two nodes have the same attributes, their values should be part
        # of the same column.
        while (new_name in self.custom_calculations.keys() or
               (self.include_defaults and new_name in self.default_metrics.keys())):
            counter += 1
            new_name = f"{col_name}_{counter}"

        if counter > 0:
            warn(f"Column '{col_name}' already exists. Using '{new_name}' instead.")
        return new_name

    def write_file(
        self,
        save_path: str | Path,
        # TODO: Adapt for new helper-function
        saving_format: Literal["csv", ".csv", "xlsx", ".xlsx"] | None = None,
        *,
        excel_engine: Literal["openpyxl", "xlsxwriter"] = 'openpyxl'
    ) -> 'GraphDescriptor':
        """Saves the dataframe at the given location in the provided format.

        The saving format will be determined dynamically based on the path suffix

        Args:
            save_path (str | Path): the saving location (and format)
            saving_format (str | None): the format of the document you want (csv or xlsx)
            excel_engine (str): the type of engine you want to use for saving the file
                in xlsx-format. Uses 'openpyxl' as default. 'openpyxl' must be installed
                in order to work correctly

        Returns:
            self

        Raises:
            TypeError if format is anything else but ".csv", ".xlsx" or no format at all.

        """
        if not hasattr(self, "dataframe"):
            self.__create_dataframe()

        # TODO: Use new helper function
        save_path, saving_format = self.__ensure_path_suffix(save_path, saving_format)

        # Ensures that the saving directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Saves the dataframe for the given type (could be match case for >= 3.10)
        if saving_format == ".csv":
            self.dataframe.to_csv(save_path, na_rep="None")

        elif saving_format == ".xlsx":
            self.dataframe.to_excel(save_path, na_rep="None", engine=excel_engine)

        else:
            raise TypeError(f"'{saving_format}' is not '.csv' or '.xlsx'")

        return self

    # TODO: deprecate with new helper function
    def __ensure_path_suffix(self, save_path: str | Path,
                             saving_format: str | None = None
                             ) -> tuple[Path, str]:
        """Ensures that the provided path has a saving format.
        Args:
            save_path (str | Path): the saving location
            saving_format (str | None): the format of the document the user provided

        Returns:
            A tuple of the provided Path leading to a file and the format of this file
        """
        # Ensures Path-operations
        if isinstance(save_path, str):
            save_path = Path(save_path)

        # If no format was specified
        if not save_path.suffix and not saving_format:
            # This should be replaced by a logger warning
            print("No saving format was provided in the 'save_path' or directly "
                  "via 'saving_format'. 'csv' was used as default")
            saving_format = ".csv"

        # 'saving_format' is always valued higher than path suffix
        if saving_format:
            # If user forgot the leading dot
            if not saving_format.startswith('.'):
                saving_format = "." + saving_format
            save_path = save_path.with_suffix(saving_format)

        return save_path, save_path.suffix
