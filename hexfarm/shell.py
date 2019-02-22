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

import shutil
import subprocess
from subprocess import PIPE
from collections.abc import MutableSet
from collections import deque, namedtuple

# -------------- External Library -------------- #

import psutil

# -------------- Hexfarm  Library -------------- #

from .util import identity, classproperty


__all__ = (
    'PIPE',
    'decoded',
    'Command',
    'man',
    'which',
    'whoami',
    'me',
    'ME',
    'ProcessStore'
)


def decoded(output, mode='stdout', encoding='utf-8'):
    """Decode Result of Command."""
    return getattr(output, mode).decode(encoding)


class Command:
    """
    Basic Command Object.

    """

    def __init_subclass__(cls, prefix=None):
        """Initialzie Command Subclasses."""
        cls.prefix = classproperty(fget=lambda c: prefix)

    @classproperty
    def prefix(cls):
        """Default Command Prefix."""
        return ''

    def __init__(self, name, *args, default_decoded=False, clean_output=identity, **kwargs):
        """Initialize Command."""
        self._name = name
        self._default_decoded = default_decoded
        self._clean_output = clean_output
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

    def _running_args(self, *args):
        """Collect Running Arguments."""
        return [self.full_name] + self.__args + list(args)

    def open(self, *args, **kwargs):
        """Open Process for Given Command."""
        return psutil.Popen(self._running_args(*args), **kwargs)

    def run(self, *args, stdout=PIPE, stderr=PIPE, result_decoded=None, clean_output=None, **kwargs):
        """Run Command."""
        result = subprocess.run(self._running_args(*args),
                                stdout=stdout,
                                stderr=stderr,
                                **self.__kwargs,
                                **kwargs)
        if result_decoded is None:
            result = result if not self._default_decoded else decoded(result)
        else:
            result = result if not result_decoded else decoded(result)
        return self._clean_output(result) if clean_output is None else clean_output(result)

    def __call__(self, *args, **kwargs):
        """Run Command."""
        return self.run(*args, **kwargs)


man = Command('man')

which = Command('which', default_decoded=True, clean_output=lambda o: o.strip())

me = whoami = Command('whoami', default_decoded=True, clean_output=lambda o: o.strip())

ME = me()


class ProcessStore(MutableSet):
    """Process Storage."""

    def __init__(self, store=None, *, history_queue=None):
        """Initialize Process Store."""
        self.store = value_or(store, set())
        # TODO: finish history queue
        if history_queue is True:
            self.history_queue = deque()
        elif history_queue:
            self.history_queue = history_queue

    def add(self, process):
        """Add Process to Store."""
        self.store.add(process)

    def discard(self, process):
        """Discard Process from Store."""
        self.store.discard(process)

    def __contains__(self, elem):
        """Check if Process is in Store."""
        # FIXME: not using good lookup algorithm
        try:
            pid = elem.pid
        except AttributeError:
            pid = elem
        for elem in self.store:
            if pid == elem.pid:
                return True
        return False

    def __iter__(self):
        """Iterate Over All Processes."""
        return iter(self.store)

    def __len__(self):
        """Length of Process Store."""
        return len(self.store)

    def add_from(self, command, *args, **kwargs):
        """Add Process from Command."""
        output = command.open(*args, **kwargs)
        self.add(output)
        return output

    def _process_map(self, process, function, *exceptions):
        """Apply Function on Process."""
        if process in self:
            if not exceptions:
                exceptions = (Exception, )
            try:
                return function(process), None
            except exceptions as initial_error:
                return function(psutil.Process(process)), initial_error
        else:
            raise KeyError('Missing Process to Kill.')

    def kill(self, process):
        """Kill Process."""
        self._process_map(process, lambda p: p.kill(), AttributeError)

    def pop_kill(self, process):
        """Kill Object and Pop from Store."""
        self.kill(process)
        self.discard(process)

    def suspend(self, process):
        """Suspend Process."""
        self._process_map(process, lambda p: p.suspend(), AttributeError)

    def pop_suspend(self, process):
        """Kill Object and Pop from Store."""
        self.suspend(process)
        self.discard(process)

    def remove_if_missing(self, process):
        """Remove Process if Missing."""
        if not process.is_running():
            self.store.remove(process)

    def sync(self, *subset):
        """Synchronize Store with Current Running Processes."""
        if subset:
            for elem in filter(lambda e: e in self, subset):
                self.remove_if_missing(elem)
        else:
            for process in list(self.store):
                self.remove_if_missing(process)
