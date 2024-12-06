# Copyright (C) 2024 dssTools Developers
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
# pylint: disable=invalid-name
"""Global settings file for dsstools.

This module sets sensible defaults for the dsstools package.

Attributes:
    log_console (bool): Log to console.
    log_file (bool): Log to file.
    log_filename (str): Filename of the log file.
    log_level (bool): Level of logging.
    log_name (str): Name of the logging output.
    logs_folder (str): Where to place logs.

    project_root (Path): Root of the project (automatically set).
    data_root (Path): Folder of the data dir (defaults to <project_root>/data)

    file_format (str): File format of the graph images.
    img_dir (str): Folder of the images output.
    dpi (int): Dots per inch of the output images. Use value of 300DPI for
        printable images. Value is irrelevant for vector-based graphics.
    canvas_height (int): Height of the resulting canvas. All other values like
        node diameter are in relation to that value.
    canvas_width (int): Width of the resulting canvas.
    axlimit (float): Limits boundaries of axis to be drawn.

    value_not_assigned (str): Default for not assigned values.
    axis_legend_loc (int): Location of the axis legend. See
        https://matplotlib.org/stable/api/legend_api.html

    label_font_size (int): Size of the labels.

    description_alpha (float): Transparency of the description text.
    description_size (int): Size of the description text.

    edge_color (str): Default edge color.
    edgewidths (float): Default edge sizes.
    arrowsize (int): Size of the arrows of directed edges.

    node_alpha (int): Transparency of nodes in the graph output.
    node_contour_colors (str): Default contour color of the nodes.
    node_contour_cmap (str,mpl.ColorMap): Colormap for mapping colors of node
        contours. For a full list see
        https://matplotlib.org/stable/tutorials/colors/colormaps.html.
    node_contour_widths (float): Default contour sizes of the nodes.
    node_size_range (tuple(int,int)): Range to which the node size is mapped to.

    cmap (mpl.ColorMap): Color map to use for coloring of sequential attributes.
    qualitative_cmap (mpl.ColorMap): Color map to use for coloring of qualitative attributes.

    colors (list(tuple(float,float,float))): Default color list as RGB codes.
    grey (tuple(float,float,float)): Default value for grey.

    NOTE: Use the following only when there are complications with your existing
    attributes:
    a_color (str): Default parameter name for the node attribute dictionary.
    a_size (str): Default parameter name for the node attribute dictionary.
    a_ccolor (str): Default parameter name for the node attribute dictionary.
    a_cwidth (str): Default parameter name for the node attribute dictionary.
    a_lcolor (str): Default parameter name for the graph attribute dictionary.
    a_lccolor (str): Default parameter name for the graph attribute dictionary.
    a_query_id (str): Default parameter name for the query attribute dictionary/tree.
"""

import logging as lg
import os
from pathlib import Path
import matplotlib as mpl

# TODO: sollen in den zentralen Logger übernommen werden
log_console = False
log_file = False
log_filename = "dsstools"
log_level = lg.WARNING
log_name = "dsstools"
logs_folder = "./logs"
###




