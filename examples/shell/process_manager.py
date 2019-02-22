#!/usr/bin/env python3
# -*- coding: utf-8 -*- #
#
# examples/shell/process_manager.py
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
Basic Process Manager Example.

"""

# -------------- Hexfarm  Library -------------- #

from hexfarm import run_main
from hexfarm.shell import Command, ProcessStore


STARTING_COUNT = 10
PROCESS_SLEEP_TIME = 2
FINISH_AFTER = 100


@run_main()
def main(argv):
    """Simple Process Manager."""
    command = Command('echo', '"hello there...";', f'sleep {PROCESS_SLEEP_TIME};')
    processes = ProcessStore()
    for _ in range(STARTING_COUNT):
        processes.add_from(command)
    print(processes)

    counter = 0
    while counter < FINISH_AFTER:
        if not processes:
            processes.add_from(command)
        print(processes)
        counter += 1
