# Copyright (C) 2024 dssTools Developers
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Module for mapping values onto colors and sizes."""

from __future__ import annotations

import logging
import math
import warnings
from abc import ABC, abstractmethod
from typing import Callable, Iterator, Mapping, TypeVar

import matplotlib as mpl
import matplotlib.colors as mcolors
import networkx as nx
import numpy as np
from matplotlib.colors import Colormap
from networkx.classes.reportviews import InEdgeDataView, OutEdgeDataView

from .attrs import Code
from .supplier import Supplier, ElementAttribute, StructuralAttribute, Percentile

# See
# https://stackoverflow.com/questions/60616802/how-to-type-hint-a-generic-numeric-type-in-python
Numeric = TypeVar("Numeric", int, float)
StrNumeric = TypeVar("StrNumeric", int, float, str)
NxElementView = TypeVar("NxElementView", OutEdgeDataView, InEdgeDataView, Iterator[tuple])

__all__ = [
    "filtering",
    "fixed",
    "percentile",
    "qualitative",
    "sequential",
]

SCALABLE_COLORMAPS = [
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "cividis",
    "Greys",
    "Purples",
    "Blues",
    "Greens",
    "Oranges",
    "Reds",
    "YlOrBr",
    "YlOrRd",
    "OrRd",
    "PuRd",
    "RdPu",
    "BuPu",
    "GnBu",
    "PuBu",
    "YlGnBu",
    "PuBuGn",
    "BuGn",
    "YlGn",
    "binary",
    "gist_yarg",
    "gist_gray",
    "gray",
    "bone",
    "pink",
    "spring",
    "summer",
    "autumn",
    "winter",
    "cool",
    "Wistia",
    "hot",
    "afmhot",
    "gist_heat",
    "copper",
]

def supplier_helper(attr):
    """Turns attribute into a Supplier if it not one already. First checks to
    see if the attribute is a StructuralAttribute to avoid obsolete values by
    always recalculating StructuralAttributes (e.g. degree, betweenness, etc.).
    If it is not a StructuralAttribute it will be processed as an
    ElementAttribute, which are graph attributes.

    Args:
        attr: attribute to be turned into a Supplier

    Returns: Supplier
    """
    if isinstance(attr, str):
        if attr in StructuralAttribute.ATTRIBUTES:
            return StructuralAttribute(attr)
        else:
            return ElementAttribute(attr)
    elif isinstance(attr, Supplier):
        return attr
    else:
        raise ValueError(
            "Invalid attribute. Pass an graph attribute name as string or a Supplier object"
        )

def parse_color(value):
    """Determine whether the value is a color.

    If it is a color the corresponding hex value will be returned. Otherwise,
    the value is returned unchanged.

    Args:
        value:

    Returns:
        Either returns a HEX color code or the value itself if no parsing was possible.
    """
    if mcolors.is_color_like(value):
        return mcolors.to_hex(value)
    return value

def parse_colormap(cmap: str | Colormap, acceptable_colormaps):
    """Determine whether the value is an acceptable colormap.

    If it is a color the corresponding hex value will be returned.  Otherwise,
    the value is returned unchanged.

    Args:
        cmap: Colormap or string of a  colormap

    Returns:
        Colormap
    """
    if isinstance(cmap, str):
        if cmap in acceptable_colormaps:
            return mpl.colormaps[cmap]

    if isinstance(cmap, Colormap):
        return cmap

    raise ValueError(
        "Invalid colormap. Pass a colormap object or one of these strings:"
        + str(acceptable_colormaps)
    )


##TOD: create supplier/mapping model where raw input data/data from another dataset is extracted (supplier)
# #pass to all Mappings except Fixed
# #supplier ex. ScalableAttribute, make one for scale(replace preprocessor), make one for percentile(minimally change percentile)
# #create FilterMapping

class GenericMapping(ABC):
    """Generic Interface for mapping visual attributes to graph elements
    values."""

    def __init__(self):
        self. supplier  = None
        self.fallback = None

    @abstractmethod
    def get(self, graph_element: NxElementView, graph: nx.Graph) -> dict:
        """
        Args:
            graph_element: NxElementView
            graph: nx.Graph
        Returns:
            A dictionary with graph_element as the keys and the value as visual mapping.
        """

    def __repr__(self):
        return str(self)


class FixedValue(GenericMapping):
    """Class for setting a singular fixed value to all items.

    Args:
        value: Set a value, either a numeric type or a color string.
    """

    __value = None

    def __init__(self, value: StrNumeric):
        super().__init__()
        self.__value = parse_color(value)

    def __str__(self):
        return f"fixed value: '{self.__value}'"

    def get(
        self, graph_element: NxElementView, graph: nx.Graph
    ) -> dict:
        """Get the fixed value for all items in the graph element.

        Args:
            graph_element: NxElementView
            graph: nx.Graph

        Returns:
            A dictionary with the key from graph as the key and value as the value
        """
        try:
            return {i[0]: self.__value for i in graph_element}
        except TypeError:
            return {i: self.__value for i in graph_element}


def generate_mapping(values: list) -> dict:
    # generates int for every unique attribute and adds it to a dictionary of value:int
    mapping = {}
    counter = 1

    for i in values:
        if i not in mapping:
            mapping[i] = counter
            counter += 1
    return mapping


class Qualitative(GenericMapping):
    """Class for assigning a value based on attributes in graph elements."""

    QUALITATIVE_COLORMAPS = [
        "Pastel1",
        "Pastel2",
        "Paired",
        "Accent",
        "Dark2",
        "Set1",
        "Set2",
        "Set3",
        "tab10",
        "tab20",
        "tab20b",
        "tab20c",
    ]

    def __init__(
        self, supplier: Supplier, mapping: Mapping | None = None, *, cmap=None
    ):
        """Assign a value to the items in the graph element attributes.

        Args:
            supplier: Supplier The raw graph attributes on which to base the mapping
            mapping: Mapping: The mapping with the keys as the values of the graph element attribute
            and the values as the desired visual values
        """
        super().__init__()

        if mapping is None and cmap is None:
            raise ValueError("At least either colormap or mapping is required.")

        if mapping is not None and cmap is not None:
            raise ValueError(
                "Number of valid mappings exceeded. Pass only a vaild mapping or only a valid colormap"
            )
        self.supplier = supplier
        self.mapping = mapping
        self.colormap = cmap

    def __str__(self):
        # TODO Move to supplier?
        if self.colormap is not None:
            return f"scaling: on '{self.supplier}' with {self.colormap}"
        return f"scaling: on '{self.supplier}' with {self.mapping}"

    def get(self, graph_element: NxElementView, graph) -> dict:
        """Get the values in the graph element based on the attribute mapping.

        Args:
            graph_element: NxElementView
            graph: nx.Graph

        Returns:
            Dict with the keys as the index of the graph element
            and the values as the desired visual values based on the attribute
        """

        #attributes = {i: k.get(self.attribute_key) for i, k in graph_element}
        attributes = self.supplier._get_values(graph_element, graph)
        mapping = (
            self.mapping
            if self.mapping is not None
            else (generate_mapping(list(attributes.values())))
        )
        if self.colormap is not None:
            self.colormap = parse_colormap(self.colormap, Qualitative.QUALITATIVE_COLORMAPS)
            if len(mapping) > len(self.colormap.colors):
                raise ValueError(
                    "Number of attributes exceeds number of available colors."
                )

            mapping = {
                i: mcolors.rgb2hex(self.colormap.colors[k - 1])
                for i, k in mapping.items()
            }

        return {i: parse_color(mapping[k]) for i, k in attributes.items()}


class Sequential(GenericMapping, ABC):
    """Abstract class for getting visual attributes according to different
    scales."""

    post_processor: Callable[[float], object]
    #LIN = lambda x: x
    #EXP = lambda x: ((math.e ** x) - 1) / (math.e - 1),
    #LOG = lambda x: math.log1p(math.e-x)*x

    def __init__(self, supplier: Supplier,
                 scale: str | Callable[[float], float] = "lin", *,
                 out_range: tuple[Numeric, Numeric], in_range: tuple | None = None,
                 fallback: StrNumeric | None = None,
                 post_processor: Callable = lambda x: x):
        """

        Args:
            *:
            in_range: tuple of the min and max values of the set before normalization
            out_range: tuple of the min and max values of the final scale
            fallback: the visual value for none
            supplier: Supplier The raw graph attributes on which to base the mapping, must have numeric values
            post_processor: function applied to the values after scaling (e.g. colormapping, conversion)
        """
        super().__init__()
        self.in_range = in_range
        self.out_range = out_range

        fallback = (
            fallback if fallback is not None else (out_range[0] / 2.0)
        )

        if isinstance(fallback, (int, float)):
            if out_range[0] <= fallback <= out_range[1]:
                warnings.warn(
                    "None values are within out range, will not be distinct",
                    stacklevel=4,
                )

        self.fallback = parse_color(fallback)

        supplier._set_fallback(fallback)


        self.supplier = supplier
        if scale == "lin":
            self.scale = lambda x: x
        elif scale == "exp":
            self.scale = lambda x: ((math.e ** x) - 1) / (math.e - 1)
        elif scale == "log":
            self.scale = lambda x: math.log1p(math.e-x)*x
        elif isinstance(scale, Callable):
            self.scale = scale
        else:
            raise ValueError("The given scaling strategy is not valid.",
                             "Pass either 'lin', 'exp', 'log' or a custom scaling lambda.")

        self.post_processor = post_processor


    def __str__(self):
        return f"scaling: '{self.supplier}' within {self.out_range}"

    # private static method
    def __get_in_range(self, values):
        """Calculate the in range by determining the min/max of the graph
        element.

        The value is returned after applying the appropriate scalable attribute
        strategy.

        Args:
            values: list of values from the graph element

        Returns:
            Tuple for the min/max range for normalization
        """
        if self.in_range is not None:
            return self.in_range


        values = [value for value in values if value is not None and isinstance(value, (int, float))]

        if all(v is None for v in values):
            raise ValueError(f"No valid values for \"{self.supplier.keyword}\" found. Try checking that the keyword is correct. The keyword must reference numeric values.")


        in_min: float = np.nanmin(values)
        in_max: float = np.nanmax(values)

        if in_max == 0:
            warnings.warn(
                "Original values are all 0. Ensure that your attribute is correct.",
                stacklevel=4,
            )


        return (in_min, in_max)

    # hook method
    # @abstractmethod
    def _scale(self, value):
        """Scale value based on custom scale.

        Args:
            value: float

        Returns:
            custom_scale(value)
        """
        return self.scale(value)


    def get(self, graph_element: NxElementView, graph: nx.Graph) -> dict:
        """Get the values by normalizing the supplier values then applying the
        scale.

        If all values are the same, the average of the out_range will be applied to all
        values.

        Args:
            graph_element: NxElementView
            graph: nx Graph

        Returns:
            dict with the keys as the index of the graph element
            and the values as the desired visual values based on scale
        """

        #super.get(graph_element, graph)

        values = self.supplier._get_values(graph_element, graph)

        in_range = self.__get_in_range(values.values())
        in_min, in_max = in_range

        out_min, out_max = self.out_range

        scaled_iterator = {}

        for node, value in values.items():
            if value is None:
                scaled_iterator[node] = self.fallback

            elif in_max == in_min:
                logging.info(
                    "All mapped values are equal, average of out_range used for mapping."
                )
                scaled_iterator[node] = self.post_processor((out_max+out_min)/2)
# TODO scale after normalization?/colormap is not using max value
            elif in_max != in_min:
                raw_factor = (value - in_min) / (in_max - in_min)
                scaled_iterator[node] = self.post_processor(
                    out_min + self._scale(raw_factor) * (out_max - out_min)
                )

        return scaled_iterator

    def also(self, preprocessor: Callable[[float], float]):
        """Helper function for easier usage of mapping by users.

        Args:
            preprocessor: function that may need to be called before scaling
            occurs (sqrt for node radius calculation)

        Returns:
            Sequential
        """
        return Sequential(
            self.supplier,
            out_range=self.out_range,
            scale=lambda x: self.scale(preprocessor(x)),
            fallback=self.fallback,
            post_processor=self.post_processor,
        )

class Filter(GenericMapping):
    """Class for assigning new visual attributes according to a filter
    condition."""

    def __init__(self, base: GenericMapping, supplier: Supplier,
                 new_mapping: GenericMapping, predicate: Callable = lambda: True):
        """

        Args:
            base: the original Mapping whose values will be assigned if the supplier value evaluates to False
            supplier: the Supplier that provides the values to be evaluated by the predicate
            new_mapping: the new Mapping whose values will be assigned if the supplier value evaluates to True
            predicate: the expression to evaluate the Supplier, must return a boolean
        """
        super().__init__()
        self.supplier = supplier
        self.base = base
        self.new_value = new_mapping
        self.predicate = predicate
        self.supplier._set_fallback(self.base.fallback)

    def get(self, graph_element: NxElementView, graph: nx.Graph) -> dict:
        """Get the visual values of the graph element based on the Supplier
        values filtered by the predicate. If the predicate is True the value of
        the new Mapping is applied, keyed by node. If the predicate is False
        the value of the base Mapping is applied, keyed by node. If the base
        mapping contains a fallback, the nodes with the fallback value will
        retain that value.

        Args:
            graph_element: NxElementView
            graph: nx.Graph

        Returns:
            Dict with the keys as the index of the graph element
            and the values as the desired visual values based on the predicate
        """
        filter_values = self.supplier._get_values(graph_element, graph)
        new_mapping_values = self.new_value.get(graph_element, graph)
        base_values = self.base.get(graph_element, graph)
        filtered_mapping = {}

        for node, value in filter_values.items():
            if self.predicate(value) and base_values[node] != self.supplier.fallback:
                filtered_mapping[node] = new_mapping_values[node]
            else:
                filtered_mapping[node] = base_values[node]

        if filtered_mapping == base_values:
            warnings.warn(
                "No changes were applied.",
                stacklevel=4,
            )

        return filtered_mapping



def fixed(value):
    """Set a fixed value, that is constant across all items in the chosen graph
    element.

    Args:
        value: v

    Returns:
        FixedValue

    Examples:
        ``` python
        ig.nodes.set_sizes(fixed(75))
        # the size of all nodes is now 75

        ig.edges.set_colors("green")
        # the color of all nodes is now green
        ```
    """
    return FixedValue(value)


def qualitative(attr: str | Code, mapping: dict | None = None, *, cmap=None):
    """Use an attribute or colormap as value.

    Args:
        attr: str name of the category
        mapping: dict of category values as the key and desired values as the values
        cmap: str of a valid colormap or colormap object

    Returns:
        Nominal

    Examples:
        ``` python
        G.add_node("a", pet="dog")
        G.add_node("b", pet="cat")

        ig.nodes.set_colors(qualitative("rating", {"cat": "red", "dog": "green"}))
        # color for node "a" is now "green" and "red" for node "b"

        ig.nodes.set_colors(qualitative("rating", cmap="Pastel1"))
        # color for node "a" is now the first color in the Pastel1 colormap and the second color for node "b"
        ```
    """
    supplier = supplier_helper(attr)
    return Qualitative(supplier, mapping, cmap=cmap)


def sequential(
    attr: str,
    scale: str | Callable = "lin",
    out_range=None,
    in_range=None,
    fallback=None,
    cmap=None,
):
    """Scale on graph element or structural graph attributes.

    Args:
        *:
        attr: str name of graph element or structural graph attribute to be scaled
        scale: scale on which the values should be assigned
        out_range: tuple of the min and max values of the final scale
        in_range: tuple of the min and max values of the set before normalization
        fallback: a color value or numeric value for None values

    Returns:
        Sequential


    Examples:
        ``` python
        G.add_node("a", rating=3)
        G.add_node("b", rating=7)

        ig.nodes.set_sizes(sequential("degree", "log", out_range=(12, 36), fallback=5))

        ig.nodes.set_sizes(sequential("rating", linear(), out_range=(12, 36), fallback=5))

        ig.nodes.set_colors(sequential("rating", fallback="orange", cmap="viridis"))

        ```
    """

    supplier = supplier_helper(attr)

    if out_range is not None and out_range[0] > out_range[1]:
        raise ValueError("out_range min must be smaller than out_range max")

    if cmap is not None:
        parsed_colormap = parse_colormap(cmap, SCALABLE_COLORMAPS)
        fallback = (
            fallback
            if fallback is not None
            else mcolors.rgb2hex(tuple(mcolors.Colormap.get_bad(parsed_colormap)))
        )
        # default colormap none/bad value is transparent. WE DO NOT ALLOW TRANSPARENT AS A VAILD VALUE FOR NONE FALLBACKS!
        if fallback == "#000000":
            logging.info(
                "#000000 (transparent) is not an acceptable fallback. It has been changed to lightgray."
            )

        fallback = fallback if fallback != "#000000" else "lightgray"

        out_range = out_range if out_range is not None else [0, 1]

        if out_range[0] < 0 or out_range[1] > 1:
            raise ValueError(
                "out_range must be between 0-1. The valid range for a colormap is 0-1. Setting an out_range subsets the colormap."
            )

        return Sequential(
            supplier,
            out_range=out_range,
            fallback=fallback,
            scale=scale,
            post_processor=lambda c: mcolors.rgb2hex(parsed_colormap(c)),
        )
    # only colormaps can have out_range as none
    if out_range is None:
        raise ValueError(
            "out_range cannot be None. If setting the out_range for alphas, set between 0-1."
        )

    return Sequential(
        supplier,
        out_range=out_range,
        scale=scale,
        fallback=fallback,
    )

def percentile(base: GenericMapping, new_values: GenericMapping, attr: str|Supplier, perc_range: tuple = None, method: str="linear"):
    """

    Args:
        base: the Mapping, whose values are assigned to the node if the attr values are inside the perc_range
        new_values: the Mapping, whose values are assigned to the node if the attr values are outside the perc_range
        attr: the attribute with which the percentile is calculated, must contain numeric values
        perc_range: tuple of min and max range for the percentile calculation, must be between 0 and 100
        method: str, optional, default "linear"
            This parameter specifies the method to use for estimating the
            percentile.  There are many different methods, some unique to NumPy.
            See the notes for explanation.  The options sorted by their R type
            as summarized in the H&F paper [1]_ are:

            1. 'inverted_cdf'
            2. 'averaged_inverted_cdf'
            3. 'closest_observation'
            4. 'interpolated_inverted_cdf'
            5. 'hazen'
            6. 'weibull'
            7. 'linear'  (default)
            8. 'median_unbiased'
            9. 'normal_unbiased'

            The first three methods are discontinuous.  NumPy further defines the
            following discontinuous variations of the default 'linear' (7.) option:

            * 'lower'
            * 'higher',
            * 'midpoint'
            * 'nearest'

    Returns:
        Filter Mapping filtered by percentile of attr assigning values based on new_values

    Examples:
        ``` python
        G.add_node("a", rating=3)
        G.add_node("b", rating=7)

        base_mapping = sequential("rating", fallback="orange", cmap="viridis")
        new_mapping = fixed("blue")

        ig.nodes.set_colors(percentile(base_mapping, new_mapping, "degree", perc_range=(0, 50))

        ```

    """
    supplier = supplier_helper(attr)

    perc = Percentile(supplier)
    perc._set_percentile_method(method)
    perc._set_percentile_range(perc_range)

    return Filter(base, perc, new_values, predicate= lambda x:x)

def filtering(base: GenericMapping, new_values: GenericMapping, attr: str | Supplier, predicate):
    """Filter the visual values of the graph element based on the attr values.

    If the predicate is True the value of the new Mapping is applied, keyed by node. If
    the predicate is False the value of the base Mapping is applied, keyed by node. If
    the base mapping contains a fallback, the nodes with the fallback value will retain
    that value.

    Args:
        base: the original Mapping whose values will be assigned if the supplier value evaluates to False
        new_values: the new Mapping whose values will be assigned if the supplier value evaluates to True
        attr: attribute that provides the values to be evaluated by the predicate
        predicate: the expression to evaluate the attr values, must return a boolean

    Returns: Filter Mapping filtered by predicate applied to attr by assigning new_values if predicate is True and base values if predicate is False.

    Examples:
        ``` python
        G.add_node("a", rating=3, school_type="uni")
        G.add_node("b", rating=7, school_type="college")

        rating = sequential("rating", out_range=(12, 36))

        new_mapping = fixed(1)

        ig.nodes.set_sizes(filtering(rating, new_mapping, "school_type", lambda x:x is "uni"))

        sizes = a: 1, b: 36
        node a has been given the value 1 because the "school_type" is "uni"
        node b remains unchanged

        ```
    """

    supplier = supplier_helper(attr)

    def is_callable(predicate):
        if not isinstance(predicate, Callable):
            return lambda x:x is predicate
        else:
            return predicate



    return Filter(base, supplier, new_values, is_callable(predicate))

