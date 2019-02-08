#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

"""
Basic Condor PseudoDaemon Implementation.

"""

# -------------- Standard Library -------------- #

import time

# -------------- External Library -------------- #

from path import Path

# -------------- Hexfarm  Library -------------- #

from hexfarm import ME, run_main
import hexfarm.condor as condor


JOB_RANGE = 100
JOB_SLEEP = 2
MAX_JOB_COUNT = 20
QUEUE_COUNT = 2
DAEMON_SLEEP = 200

JOB_SOURCE = condor.clean_source('''

#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import time
from hexfarm import run_main

@run_main()
def main(argv):
    for x in range({job_range}):
        time.sleep({job_sleep})
        print(x ** x)
    return 0

'''.format(job_range=JOB_RANGE, job_sleep=JOB_SLEEP))


def submit_jobs(job_map, max_count):
    """Submit Jobs Unitl Maximum Count."""
    while True:
        job_map.pop_completed()
        count = len(job_map)
        if count >= max_count:
            break
        print('{count} jobs running.'.format(count=count))
        if count < max_count:
            print('Submitting Jobs ...')
            job_map.submit()


@run_main()
def main(argv):
    """Simple Daemon."""
    directory = Path('.temp/simple_daemon')
    directory.makedirs_p()
    config = condor.JobConfig(path=directory / 'config.cfg')
    executable = directory / 'job.py'
    executable.remove_p()
    executable.write_text(JOB_SOURCE)
    condor.add_execute_permissions(executable)

    with config.write_mode as cfg:
        cfg.comments('Test File', 'Multiline Comment')
        cfg.initialdir = directory
        cfg.log = 'job.log'
        cfg.error = 'job_$(Cluster)_$(Process).error'
        cfg.output = 'job_$(Cluster)_$(Process).out'
        cfg.executable = executable
        cfg.getenv = True
        cfg.stream_output = True
        cfg.queue(QUEUE_COUNT)

    job_map = condor.JobMap(source_config=config)

    while True:
        print('Current Map:', job_map)
        submit_jobs(job_map, MAX_JOB_COUNT)
        print('Sleeping for {sleep} seconds ...'.format(sleep=DAEMON_SLEEP))
        time.sleep(DAEMON_SLEEP)
