# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os
import re
import logging

try:
    # Since the tests run in a container,
    # we need to exec within that container to get the cli stats
    # Docker is not shipped with the agent and this should not be used outside of the testing
    import docker
except ImportError:
    docker = None

from datadog_checks.utils.subprocess_output import get_subprocess_output

log = logging.getLogger(__file__)


class CommandLine:
    def __init__(self, config):
        self.config = config

        if self.config.docker_container:
            self.docker_container = self.config.docker_container
        else:
            self.docker_container = None

        self.cmd_path = os.path.join(self.config.mq_installation_dir, 'bin', 'runmqsc')
        self.queue_manager_name = self.config.queue_manager_name

        self.use_docker = False
        if self.docker_container and docker:
            self.use_docker = True

    def _run_command(self, cmd):
        result = None
        err = None
        if self.use_docker:
            client = docker.from_env()
            _, result = client.containers.exec_run(
                " ".join(self._mk_cmd(cmd))
            )
        else:
            result, err, _ = get_subprocess_output(self._mk_cmd(cmd), log, False)

        return result, err

    def _mk_cmd(self, cmd):
        full_cmd = [
            "echo",
            cmd
            "|",
            self.cmd_path,
            self.queue_manager_name
        ]
        return full_cmd

    def get_all_queues(self):
        cmd = ["dis", "queue('*')"]

        result, err = _run_command(cmd)
        log.warning(err)
        if err:
            raise err

        log.warning(result)
