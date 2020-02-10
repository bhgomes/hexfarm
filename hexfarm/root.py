# -*- coding: utf-8 -*- #
#
# hexfarm/root.py
#
#
# MIT License
#
# Copyright (c) 2018-2019 Brandon Gomes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
ROOT Utilities.

"""

# -------------- Standard Library -------------- #

import logging

# -------------- External Library -------------- #

from path import Path

import uproot
import uproot_methods
import histbook
import formulate

# -------------- Hexfarm  Library -------------- #

from .io import has_extension, walk_paths
from .util import try_import
from .util.functools import partial


LOGGER = logging.getLogger(__name__)


ROOT, ROOT_SUPPORT = try_import("ROOT", log_error=LOGGER.info)


if ROOT_SUPPORT:
    R = ROOT
    LOGGER.log(logging.INFO, "ROOT Enabled.")


rootpy, ROOTPY_SUPPORT = try_import("rootpy", log_error=LOGGER.info)

root_numpy, ROOT_NUMPY_SUPPORT = try_import("root_numpy", log_error=LOGGER.info)

root_pandas, ROOT_PANDAS_SUPPORT = try_import("root_pandas", log_error=LOGGER.info)

root_ufunc, ROOT_UFUNC_SUPPORT = try_import("root_ufunc", log_error=LOGGER.info)


if ROOTPY_SUPPORT:
    from rootpy.tree import Tree, TreeModel, Cut
    from rootpy.tree.categories import Categories
    from rootpy.io import root_open


if ROOT_NUMPY_SUPPORT:
    from root_numpy import root2array, array2tree, rec2array, fill_hist


def traverse_root_files(directory):
    """Collect ROOT Files."""
    for root, _, files in walk_paths(
        directory, file_predicate=partial(has_extension, "root")
    ):
        root_path = Path(root)
        yield from (root_path / name for name in files)


def chain(directory):
    """"""
    # TODO:
    return NotImplemented
