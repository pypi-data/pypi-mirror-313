# -*- coding: utf-8 -*-
# noqa: E501
# pylint: disable=C0301
"""The api-24sea package contains modules that are aimed at helping a user interact with the 24SEA API.

The modules are:

- :mod:`api_24sea.datasignals`: Contains the :class:`DataSignals` class, which
    is an accessor for transforming data signals from the 24SEA API into
    pandas DataFrames.
- :mod:`api_24sea.utils`: Contains utility functions and classes to help
    manage requests to the 24SEA API.

Besides, the package also contains the :mod:`api_24sea.version`
module, which contains the version number of the package.
"""

from . import datasignals

__all__ = ["datasignals"]

from .version import __version__ as __version__  # noqa: F401
