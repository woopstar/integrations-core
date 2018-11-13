# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import logging

log = logging.getLogger(__file__)

class Connection:
    def __init__(self):
        import pymqi
        self.pymqi = pymqi

    def get_queue_manager_connection(self, config):
        if config.ssl:
            return self.get_ssl_connection(config)
        else:
            return self.get_normal_connection(config)


    def get_normal_connection(self, config):
        if config.username and config.password:
            log.debug("connecting with username and password")
            queue_manager = self.pymqi.connect(
                config.queue_manager_name,
                config.channel,
                config.host_and_port,
                config.username,
                config.password
            )
        else:
            log.debug("connecting without a username and password")
            queue_manager = self.pymqi.connect(
                config.queue_manager_name,
                config.channel,
                config.host_and_port,
            )

        return queue_manager


    def get_ssl_connection(self, config):
        cd = self.pymqi.CD()
        cd.ChannelName = config.channel
        cd.ConnectionName = config.host_and_port
        cd.ChannelType = self.pymqi.CMQC.MQCHT_CLNTCONN
        cd.TransportType = self.pymqi.CMQC.MQXPT_TCP
        cd.SSLCipherSpec = config.ssl_cipher_spec

        sco = self.pymqi.SCO()
        sco.KeyRepository = config.key_repo_location

        queue_manager = self.pymqi.QueueManager(None)
        queue_manager.connect_with_options(config.queue_manager, cd, sco)

        return queue_manager
