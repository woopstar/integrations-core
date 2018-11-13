# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import copy
import sys
import logging

from os import path

from datadog_checks.utils.subprocess_output import get_subprocess_output


class Environment:
    def __init__(self, config, log):
        self.old_env = copy.deepcopy(sys.environ)
        self.log = log

        self.mq_installation_dir = config.mq_installation_dir
        self.queue_manager_name = config.queue_manager_name

    def set_env(self):
        crtmqenv_cmd = path.join(self.mq_installation_dir, 'bin', 'crtmqenv')

        cmd = [
            crtmqenv_cmd,
            '-m',
            self.queue_manager_name,
            '-k'
        ]

        output, err, _ = get_subprocess_output(cmd, self.log, False)
        if err:
            self.log.info("cannot set IBM MQ environment, attempting to run without")
            return

        split_output = output.splitlines()

        for output in split_output:
            s = output.split('=')
            name = s[0]
            value = s[1]

            sys.environ[name] = value

    def clean_env(self):
        sys.environ = self.old_env
