# -*- coding: utf-8 -*- #
#
# hexfarm/util/core.py
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
Hexfarm Core Utilities.

"""

# -------------- Standard Library -------------- #

from importlib import import_module

# -------------- External Library -------------- #

import wrapt
from box import Box, BoxList

# -------------- Hexfarm  Library -------------- #

from .functools import partial


def passf(*args, **kwargs):
    """Does Nothing."""


def identity(x):
    """Identity Function."""
    return x


def flip(f):
    """Swap Arguments."""
    return lambda left, right: f(right, left)


def map_value_or(f, value, default):
    """Return Value or Default if Value is None."""
    return f(value) if value is not None else default


def value_or(value, default):
    """Return Value or Default if Value is None."""
    return value if value is not None else default


def instance_of(types):
    """Returns Function which Checks Type."""
    return partial(flip(isinstance), types)


def subclass_of(types):
    """Returns Function which Checks Subclass."""
    return partial(flip(issubclass), types)


def make_class(name, parents=(), dct=None):
    """Build a Class."""
    return type(name, parents, value_or(dct, {}))


def subdict(d, *keys, key_filter=lambda o: o, value_filter=lambda o: o):
    """
    Return Subdictionary.
    :param d:
    :param keys:
    :param key_filter:
    :param value_filter:
    :return:
    """
    keys = set(d.keys()) - set(keys)
    out = {}
    for k in filter(key_filter, keys):
        value = d[k]
        if value_filter(value):
            out[k] = value
    return out


class classproperty(property):
    """Class Property."""

    def __get__(self, obj, objtype=None):
        """Wrap Getter Function."""
        return super().__get__(objtype)

    def __set__(self, obj, value):
        """Wrap Setter Function."""
        return super().__set__(type(obj), value)

    def __delete__(self, obj):
        """Wrap Deleter Function."""
        super().__delete__(type(obj))


def try_import(
    name, package=None, *exceptions, log_error=passf, log_success=passf, default=None
):
    """
    Attempt Package Import With Automatic Exception Handling.

    :param name:
    :param package:
    :param exceptions:
    :param log_error:
    :param log_success:
    :param default:
    :return:
    """
    if not exceptions:
        exceptions = (ImportError, ModuleNotFoundError)
    try:
        module = import_module(name, package=package)
        log_success(module)
        return module, True
    except exceptions as import_error:
        try:
            module = import_module(package)
            resource = getattr(module, name)
            log_success(resource)
            return resource, True
        except exceptions as import_error:
            log_error(import_error)
        except AttributeError as attribute_error:
            log_error(attribute_error)
        log_error(import_error)
    return default, False
