# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import copy
import os

from datadog_checks.utils.subprocess_output import get_subprocess_output


class Environment:
    def __init__(self, config, log):
        self.old_env = copy.deepcopy(os.environ)
        self.log = log

        self.mq_installation_dir = config.mq_installation_dir
        self.queue_manager_name = config.queue_manager_name

    def set_env(self):
        crtmqenv_cmd = os.path.join(self.mq_installation_dir, 'bin', 'crtmqenv')

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

            environ[name] = value

    def clean_env(self):
        os.environ = self.old_env
