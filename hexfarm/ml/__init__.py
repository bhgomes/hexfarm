# -*- coding: utf-8 -*- #
#
# hexfarm/ml/__init__.py
#
#
# MIT License
#
# Copyright (c) 2019 Brandon Gomes
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
Hexfarm Machine Learning Library.

"""

# -------------- Standard Library -------------- #

import logging

# -------------- External Library -------------- #

import keras
import torch
from torch import nn
import sonnet as snt
import tensorflow as tf
import sklearn

# -------------- Hexfarm  Library -------------- #

from ..util import try_import


LOGGER = logging.getLogger(__name__)


hep_ml, HEP_ML_SUPPORT = try_import("hep_ml", log_error=LOGGER.info)


madminer, MADMINER_SUPPORT = try_import("madminer", log_error=LOGGER.info)


if MADMINER_SUPPORT:
    import madminer.ml
