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
JOB_SLEEP = 0.5
MAX_JOB_COUNT = 5
QUEUE_COUNT = 4
DAEMON_SLEEP = 40


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


def job_submit_loop(max_job_count):
    """Submit Jobs Until Maximum Count."""
    def inner_loop(config_runner):
        count = config_runner.running_job_count
        if count >= max_job_count:
            return False
        print(f'{count} jobs running.')
        if count < max_job_count:
            print('Submitting Jobs ...')
            return True
    return inner_loop


@run_main()
def main(argv):
    """Simple Daemon."""
    directory = Path('.temp/simple_daemon')
    directory.makedirs_p()

    executable = condor.build_executable(directory / 'job.py', JOB_SOURCE)
    logfile = (directory / 'job.log').abspath()

    with condor.JobConfig(path=directory / 'config.cfg').write_mode as config:
        config.append_comments('Simple HEXFARM Pseudo Daemon', 'bhgomes')
        config.log = logfile
        config.executable = executable
        config.getenv = True
        config.stream_output = True
        config.initialdir = directory
        config.error = 'job_$(Cluster)_$(Process).error'
        config.output = 'job_$(Cluster)_$(Process).out'
        config.queue(QUEUE_COUNT)

    manager = condor.JobManager()
    runner = manager.add_config('simple_daemon', config, logfile=logfile)

    while True:
        print(f'Current Jobs: {manager.running_job_count}')
        runner.submit_while(job_submit_loop(MAX_JOB_COUNT))
        print(f'Sleeping for {DAEMON_SLEEP} seconds ...')
        time.sleep(DAEMON_SLEEP)
