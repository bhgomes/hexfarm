#!/usr/bin/env python3
# -*- coding: utf-8 -*- #
#
# examples/condor/daemon/using_simple.py
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
Basic Condor PseudoDaemon Implementation.

"""

# -------------- Hexfarm  Library -------------- #

from hexfarm import run_main, decoded
from hexfarm.io import add_execute_permissions
import hexfarm.condor as condor


@run_main()
def main(argv):
    """Build Simple Deamon from simple.py."""
    executable = 'examples/condor/daemon/simple.py'
    add_execute_permissions(executable)
    config = condor.minimal_config('simple_pseudo', executable, '.temp/simple_daemon')
    config.queue()
    runner = condor.JobManager().add_config(config.name, config, remove_completed_jobs=True)
    runner.submit()
    print('Simple Pseudo Submitted!')
    print(decoded(condor.condor_q()))
