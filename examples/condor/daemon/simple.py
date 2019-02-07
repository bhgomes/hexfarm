#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

"""
Basic Condor PseudoDaemon Implementation.

"""

# -------------- External Library -------------- #

from path import Path

# -------------- Hexfarm  Library -------------- #

from hexfarm import run_main, with_timeout
import hexfarm.condor as condor


JOB_RANGE = 100
JOB_SLEEP = 5
MAX_JOB_COUNT = 10
DAEMON_TIMEOUT = 200

JOB_SOURCE = condor.clean_source('''

#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import time
from hexfarm import run_main, with_timeout

@run_main()
def main(argv):
    for i in range({job_range}):
        time.sleep({job_sleep})
        print(i ** i)
    return 0

'''.format(job_range=JOB_RANGE, job_sleep=JOB_SLEEP))


@run_main()
def main(argv):
    """Simple Daemon."""
    config = condor.JobConfig()
    directory = Path('.temp/simple_daemon')
    directory.makedirs_p()

    executable = directory / 'job.py'
    executable.remove_p()
    executable.write_text(JOB_SOURCE)
    condor.add_execute_permissions(executable)

    with config.write_mode as cfg:
        cfg.add_comments('Test File')
        cfg.initialdir = directory
        cfg.log = directory / 'job.log'
        cfg.error = directory / 'job.error'
        cfg.out = directory / 'job.out'
        cfg.executable = executable
        cfg.queue()

    job_map = condor.JobMap(remove_completed_jobs=True)
    job_map.attach_config(config)

    while True:
        print('HERE')
        jobs_running = len(job_map)
        if jobs_running < MAX_JOB_COUNT:
            for _ in range(MAX_JOB_COUNT - jobs_running):
                job_map.submit()
        print(job_map)
        time.sleep(DAEMON_TIMEOUT)
