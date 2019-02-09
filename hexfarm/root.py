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

# -------------- External Library -------------- #

from path import Path

import uproot
import uproot_methods
import rootpy
import histbook

# -------------- Hexfarm  Library -------------- #

from .io import has_extension, walk_paths


__all__ = (
    'traverse_root_files',
    'chain'
)


def traverse_root_files(directory):
    """Collect ROOT Files."""
    for root, _, files in walk_paths(directory, file_predicate=partial(has_extension, 'root')):
        root_path = Path(root)
        yield from (root_path / name for name in files)


def chain(directory):
    """"""
    #TODO:
    return NotImplemented
