# Copyright (C) 2024 dssTools Developers
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Module containing various helper functions."""
from __future__ import annotations

import warnings
from json import JSONEncoder
from pathlib import Path

import numpy as np


def _deprecate(deprecation_warning):
    def deprecation(func):
        def deprecated_func(*args, **kwargs):
            warnings.warn(f"${func.__name__} is deprecated. ${deprecation_warning}",
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)

        return deprecated_func

    return deprecation


def ensure_file_format(path: str | Path,
                       *,
                       default_format: str,
                       format_filter: set | None = None) -> tuple[Path, str]:
    """Ensures that the provided path has a saving format and its parents exist.

    If the saving format is not in the defined format_filter, a TypeError
    will be raised.

    Args:
        path (str | Path): the path that needs to be validated
        default_format (str): the format a programmer can set that will be used as
            default, if no format was provided. Leading periods can be included.
        format_filter (set | None): this specifies a filter of accepted formats. Leading
            periods can be included. Adding the default parameter isn't mandatory, since
            it is added dynamically but should be best practice.

    Raises:
        TypeError if a filter-set was provided and the saving format from the user's
        path is not in it. The default parameter will always be part of the format
        filter since it would make no sense to not have it in there. The programmer
        should still add it explicitly for comprehension reasons

    Returns:
        the filepath and format (without leading dot) as an 2-Tuple
    """
    # Ensures Path-operations
    if isinstance(path, str):
        path = Path(path)

    # Sets leading dot for default format
    if not default_format.startswith("."):
        default_format = "." + default_format

    # Default format is always added to format filter
    if (format_filter and default_format not in format_filter
        and default_format.strip('.') not in format_filter):
        format_filter.add(default_format)

    # Ensures that the path's directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Extracts the provided saving format from path
    saving_format = path.suffix

    # If no format was specified, set to default
    if not saving_format:
        warnings.warn(f"No saving format was provided in the 'path'. Make sure your "
                      f"path looks simular to this: /your/path/file.{default_format}. "
                      f"'{default_format}' was used as default.")
        # sets the format to default (with leading dot)
        saving_format = default_format

        # Add the new format (this is an extra step, because saving format needs to be
        # set specifically for later checks)
        path = path.with_suffix(saving_format)  # saving_format needs leading dot

    # Cleans suffix from dot for more usability when checking for filter
    cleaned_saving_format = saving_format.strip(".")

    # If filter specified, filter for clarified formats
    if format_filter:
        # Makes sure that is doesn't matter weither or not leading dot is included
        if saving_format not in format_filter and cleaned_saving_format not in format_filter:
            raise TypeError(f"Your format '{saving_format}' is not in: {format_filter}")

    return path, cleaned_saving_format


class NumpyEncoder(JSONEncoder):
    """Json encoder for numpy arrays."""
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, (np.ndarray)):
            return o.tolist()
        return JSONEncoder.default(self, o)
