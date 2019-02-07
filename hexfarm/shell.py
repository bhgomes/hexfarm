# -*- coding: utf-8 -*- #
#
# hexfarm/shell.py
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
Utilities for Shell Processes.

"""

# -------------- Standard Library -------------- #

import subprocess

# -------------- Hexfarm  Library -------------- #

from .util import classproperty


__all__ = ('decoded',
           'Command',
           'whoami')


def decoded(output, mode='stdout', encoding='utf-8'):
    """Decode Result of Command."""
    return getattr(output, mode).decode(encoding)


class Command:
    """
    Basic Command Object.

    """

    @classproperty
    def prefix(cls):
        """Command Prefix."""
        return ''

    def __init__(self, name, *args, default_decoded=False, **kwargs):
        """Initialize Command."""
        self._name = name
        self._default_decoded = default_decoded
        self.__args = list(args)
        self.__kwargs = kwargs

    @property
    def name(self):
        """Get Name of Command."""
        return self._name

    @property
    def full_name(self):
        """Get Full Name of Command."""
        return type(self).prefix + self.name

    def run(self, *args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, result_decoded=None, **kwargs):
        """Run Command."""
        result = subprocess.run([self.full_name] + self.__args + list(args),
                                stdout=stdout,
                                stderr=stderr,
                                **self.__kwargs,
                                **kwargs)
        if result_decoded is None:
            return result if not self._default_decoded else decoded(result)
        else:
            return result if not result_decoded else decoded(result)

    def __call__(self, *args, **kwargs):
        """Run Command."""
        return self.run(*args, **kwargs)

    def help(self, *args, **kwargs):
        """Print Help Mode of Command."""
        return self('--help', *args, **kwargs)

    def man(self, *args, **kwargs):
        """Print Man Pages of Command."""
        return subprocess.run(['man', self.full_name] + list(args), **kwargs)


whoami = Command('whoami', default_decoded=True)
