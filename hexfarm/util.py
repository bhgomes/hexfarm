# -*- coding: utf-8 -*- #
#
# hexfarm/util.py
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
Hexfarm Utilities.

"""

__all__ = ('value_or', 'instance_of', 'subclass_of', 'subdict', 'classproperty')


def value_or(value, default):
    """Return Value or Default if Value is None."""
    return value if value is not None else default


def instance_of(types):
    """Returns Function which Checks Type."""
    def inner(obj):
        return isinstance(obj, types)
    return inner


def subclass_of(types):
    """Returns Function which Checks Subclass."""
    def inner(obj):
        return issubclass(obj, types)
    return inner


def subdict(d, *keys, key_filter=lambda o: o, value_filter=lambda o: o):
    """Return Subdictionary"""
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
