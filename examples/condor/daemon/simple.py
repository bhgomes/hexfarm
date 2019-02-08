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

from hexfarm import run_main
import hexfarm.condor as condor


JOB_RANGE = 100
JOB_SLEEP = 5
MAX_JOB_COUNT = 10
DAEMON_TIMEOUT = 200

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
        cfg.getenv = True
        cfg.stream_output = True
        cfg.initialdir = directory
        cfg.log = 'job.log'
        cfg.error = 'job.error'
        cfg.output = 'job.out'
        cfg.executable = executable
        cfg.queue()

    job_map = condor.JobMap(remove_completed_jobs=True, source_config=config)

    while True:
        jobs_running = len(job_map)
        if jobs_running < MAX_JOB_COUNT:
            for _ in range(MAX_JOB_COUNT - jobs_running):
                job_map.submit()
        print(job_map)
        time.sleep(DAEMON_TIMEOUT)
