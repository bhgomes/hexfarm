# -*- coding: utf-8 -*- #
#
# hexfarm/experimental/condor.py
#
#
# MIT License
#
# Copyright (c) 2018 Brandon Gomes
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
Utilities for the HTCondor Parallel Computing Framework.

"""

# -------------- Standard Library -------------- #

import logging
import shlex
import subprocess
from collections import UserList
from contextlib import contextmanager
from dataclasses import dataclass
from inspect import cleandoc as clean_whitespace

# -------------- External Library -------------- #

from aenum import Enum, AutoValue

# -------------- Hexfarm  Library -------------- #

from ..util import classproperty


logger = logging.Logger()


try:
    import htcondor as ht
except Exception:
    logger.info('HTCondor could not be imported.')


class Command:
    """
    Basic Command Object.

    """

    PREFIX = 'condor_'

    def __init__(self, name, *args, **kwargs):
        """Initialize Command."""
        self.name = name
        self.__args = list(args)
        self.__kwargs = kwargs

    @property
    def full_name(self):
        """Get Full Name of Command."""
        return self.__class__.PREFIX + self.name

    def run(self, *args, **kwargs):
        """Run Command."""
        return subprocess.run([self.full_name] + self.__args + list(args), **self.__kwargs, **kwargs)

    def __call__(self, *args, **kwargs):
        """Run Command."""
        return self.run(*args, **kwargs)

    def help(self, *args, **kwargs):
        """Print Help Mode of Command."""
        return self('--help', *args, **kwargs)

    def man(self, *args, **kwargs):
        """Print Man Pages of Command."""
        return subprocess.run(['man', self.full_name] + list(args), **kwargs)


advertise = Command('advertise')

c_gahp = Command('c-gahp')

c_gahp_worker_thread = Command('c-gahp_worker_thread')

checkpoint = Command('checkpoint')

check_userlogs = Command('check_userlogs')

ckpt_server = Command('ckpt_server')

cod = Command('cod')

collector = Command('collector')

compile = Command('compile')

configure = Command('configure')

config_val = Command('config_val')

continue_ = Command('continue')

credd = Command('credd')

dagman = Command('dagman')

drain = Command('drain')

fetchlog = Command('fetchlog')

findhost = Command('findhost')

ft_gahp = Command('ft-gahp')

gather_info = Command('gather_info')

gridmanager = Command('gridmanager')

gridshell = Command('gridshell')

had = Command('had')

history = Command('history')

hold = Command('hold')

init = Command('init')

install = Command('install')

kbdd = Command('kbdd')

master = Command('master')

master_s = Command('master_s')

negotiator = Command('negotiator')

off = Command('off')

on = Command('on')

ping = Command('ping')

power = Command('power')

preen = Command('preen')

prio = Command('prio')

procd = Command('procd')

q = Command('q')

qedit = Command('qedit')

qsub = Command('qsub')

reconfig = Command('reconfig')

release = Command('release')

replication = Command('replication')

reschedule = Command('reschedule')

restart = Command('restart')

rm = Command('rm')

root_switchboard = Command('root_switchboard')

router_history = Command('router_history')

router_q = Command('router_q')

router_rm = Command('router_rm')

run = Command('run')

schedd = Command('schedd')

set_shutdown = Command('set_shutdown')

shadow = Command('shadow')

shadow_s = Command('shadow_s')

# shadow.std

ssh_to_job = Command('ssh_to_job')

startd = Command('startd')

starter = Command('starter')

# starter.std

stats = Command('stats')

status = Command('status')

store_cred = Command('store_cred')

submit = Command('submit')

submit_dag = Command('submit_dag')

suspend = Command('suspend')

tail = Command('tail')

test_match = Command('test_match')

transferd = Command('transferd')

transfer_data = Command('transfer_data')

updates_stats = Command('updates_stats')

userlog = Command('userlog')

userlog_job_counter = Command('userlog_job_counter')

userprio = Command('userprio')

vacate = Command('vacate')

vacate_job = Command('vacate_job')

version = Command('version')

vm_gahp = Command('vm-gahp')

vm_gahp_vmware = Command('vm-gahp-vmware')

vm_vmware = Command('vm_vmware')

# vm_vmware.pl

wait = Command('wait')

who = Command('who')


# TODO:
# locals().extend(map(Command, command_list))


class Universe(Enum, settings=AutoValue):
    """
    Condor Universe Enum.

    """

    Vanilla, Standard, Scheduler, Local, Grid, Java, VM, Parallel, Docker


@dataclass
class Notification:
    """
    Notification Structure.

    """

    class Status(Enum, settings=AutoValue):
        """Notification Status."""
        Always, Complete, Error, Never

    email: str
    status: Status

    def __str__(self):
        """"""
        return ''


class FileTransferMode(Enum, settings=AutoValue):
    """
    File Transfer Mode.

    """

    Yes, No, IfNeeded


class TransferOutputMode(Enum, settings=AutoValue):
    """
    Transfer Output Mode.

    """

    OnExit, OnExitOrEvict


class JobConfig(UserList):
    """
    Job Configuration Structure.

    """

    @classproperty
    def command_names(cls):
        """Get Possible Command Names for Condor Config File."""
        if not hasattr(cls, '_cmd_names'):
            cls._cmd_names = ('arguments',
                              'environment',
                              'error',
                              'executable',
                              'getenv',
                              'input',
                              'log',
                              'log_xml',
                              'notification',
                              'output',
                              'priority',
                              'queue',
                              'universe',
                              'rank',
                              'request_cpus',
                              'request_disk',
                              'request_memory',
                              'request_',
                              'requirements',
                              'dont_encrypt_input_files',
                              'dont_encrypt_output_files',
                              'encrypt_execute_directory',
                              'encrypt_input_files',
                              'encrypt_output_files',
                              'max_transfer_input_mb',
                              'max_transfer_output_mb',
                              'output_destination',
                              'should_transfer_files',
                              'skip_filechecks',
                              'stream_error',
                              'stream_input',
                              'stream_output',
                              'transfer_executable',
                              'transfer_input_files',
                              'transfer_output_files',
                              'transfer_output_remaps',
                              'when_to_transfer_output',
                              'max_retries',
                              'retry_until',
                              'success_exit_code',
                              'hold',
                              'keep_claim_idle',
                              'leave_in_queue',
                              'next_job_start_delay',
                              'on_exit_hold',
                              'on_exit_hold_reason',
                              'on_exit_hold_subcode',
                              'on_exit_remove',
                              'periodic_hold',
                              'periodic_hold_reason',
                              'periodic_hold_subcode',
                              'periodic_release',
                              'periodic_remove',
                              'allow_startup_script',
                              'append_files',
                              'buffer_files',
                              'buffer_size',
                              'buffer_block_size',
                              'compress_files',
                              'fetch_files',
                              'file_remaps',
                              'local_files',
                              'want_remote_io',
                              'azure_admin_key',
                              'azure_admin_username',
                              'azure_auth_file',
                              'azure_image',
                              'azure_location',
                              'azure_size',
                              'batch_queue',
                              'boinc_authenticator_file',
                              'cream_attributes',
                              'delegate_job_GSI_credentials_lifetime',
                              'ec2_access_key_id',
                              'ec2_ami_id',
                              'ec2_availability_zone',
                              'ec2_block_device_mapping',
                              'ec2_ebs_volumes',
                              'ec2_elastic_ip',
                              'ec2_iam_profile_arn',
                              'ec2_iam_profile_name',
                              'ec2_instance_type',
                              'ec2_keypair',
                              'ec2_keypair_file',
                              'ec2_parameter_names',
                              'ec2_parameter_',
                              'ec2_secret_access_key',
                              'ec2_security_groups',
                              'ec2_security_ids',
                              'ec2_spot_price',
                              'ec2_tag_names',
                              'ec2_tag_',
                              'want_name_tag',
                              'ec2_user_data',
                              'ec2_user_data_file',
                              'ec2_vpc_ip',
                              'ec2_vpc_subnet',
                              'gce_auth_file',
                              'gce_image',
                              'gce_json_file',
                              'gce_machine_type',
                              'gce_metadata',
                              'gce_metadata_file',
                              'gce_preemptible',
                              'globus_rematch',
                              'globus_resubmit',
                              'globus_rsl',
                              'grid_resource',
                              'keystore_alias',
                              'keystore_file',
                              'keystore_passphrase_file',
                              'my_proxy_credential_name',
                              'my_proxy_host',
                              'my_proxy_new_proxy_lifetime',
                              'my_proxy_password',
                              'my_proxy_refresh_threshold',
                              'my_proxy_server_dn',
                              'nordugrid_rsl',
                              'transfer_error',
                              'transfer_input',
                              'transfer_output',
                              'use_x509userproxy',
                              'x509userproxy',
                              'hold_kill_sig',
                              'jar_files',
                              'java_vm_args',
                              'machine_count',
                              'remove_kill_sig',
                              'vm_disk',
                              'vm_checkpoint',
                              'vm_macaddr',
                              'vm_memory',
                              'vm_networking',
                              'vm_networking_type',
                              'vm_no_output_vm',
                              'vm_type',
                              'vmware_dir',
                              'vmware_should_transfer_files',
                              'vmware_snapshot_disk',
                              'xen_initrd',
                              'xen_kernel',
                              'xen_kernel_params',
                              'xen_root',
                              'docker_image',
                              'accounting_group',
                              'accounting_group_user',
                              'concurrency_limits',
                              'concurrency_limits_expr',
                              'copy_to_spool',
                              'coresize',
                              'cron_day_of_month',
                              'cron_day_of_week',
                              'cron_hour',
                              'cron_minute',
                              'cron_month',
                              'cron_prep_time',
                              'cron_window',
                              'dagman_log',
                              'deferral_prep_time',
                              'deferral_time',
                              'deferral_window',
                              'description',
                              'email_attributes',
                              'image_size',
                              'initialdir',
                              'job_ad_information_attrs',
                              'job_batch_name',
                              'job_lease_duration',
                              'job_machine_attrs',
                              'want_graceful_removal',
                              'kill_sig',
                              'kill_sig_timeout',
                              'load_profile',
                              'match_list_length',
                              'job_max_vacate_time',
                              'max_job_retirement_time',
                              'nice_user',
                              'noop_job',
                              'noop_job_exit_code',
                              'noop_job_exit_signal',
                              'remote_initialdir',
                              'rendezvousdir',
                              'run_as_owner',
                              'stack_size',
                              'submit_event_notes')
        return cls._cmd_names

    @classmethod
    def load_from(cls, path, opener=open, *args, clean_input=lambda o: o.strip(), **kwargs):
        """Load Job Config from File."""
        config = cls(path=path)
        with opener(path, *args, **kwargs) as f:
            config.extend(clean_input(line) for line in f)
        return config

    def __init__(self, *lines, path=''):
        """Initialize Config."""
        super().__init__(*lines)
        self.path = path
        self._write_mode = False

    @property
    def lines(self):
        """Alias to Inner Structure."""
        return self.data

    @property
    def lines(self, new_lines):
        """Set Inner Structure."""
        self.data = new_lines

    def to_text(self, *, add_newline=True):
        """Return Config as Multiline Text."""
        base = '\n' if add_newline else ''
        return base.join(self)

    @property
    def as_text(self):
        """Return Config as Multiline Text."""
        return self.to_text()

    def submit(self, *options, **kwargs):
        """Submit Job From Config."""
        self.result = Command('submit')(self.as_text, *options, **kwargs)
        return self.result

    def __repr__(self):
        """Representation of Config File."""
        return f'JobConfig({"path=" + str(path) + "," if path else ""}...)'

    def __str__(self):
        """Get Config File as a String."""
        return self.as_text

    def _make_kv_string(self, key, value):
        """Make Key-Value String."""
        return str(key) + '=' + str(value)

    def add_keyvalues(self, **kwargs):
        """Append Key Value Pairs to Config."""
        self.extend(map(self._make_kv_string, kwargs.items()))

    def append(self, value):
        """Append to Config."""
        if not isinstance(value, str):
            super().append(str(value))
        else:
            super().append(value)

    def extend(self, other):
        """Extend Config by another Config."""
        if not isinstance(other, type(self)):
            super().extend(map(str, other))
        else:
            super().extend(other)

    def __add__(self, other):
        """Create Sum of Config."""
        if not isinstance(other, type(self)):
            return super().__add__(map(str, other))
        return super().__add__(other)

    def __iadd__(self, other):
        """Add to Config In Place."""
        self.extend(other)
        return self

    @contextmanager
    def write_mode(self):
        """Use writing mode to add lines to file."""
        try:
            self._write_mode = True
            yield self
        finally:
            self._write_mode = False

    def __setattr__(self, name, value):
        """Set attributes."""
        if self._write_mode and name in type(self).command_names:
            self.append(self._make_kv_string(name, value))
        else:
            self.__dict__[name] = value
