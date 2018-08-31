# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from __future__ import division

from datadog_checks.checks import AgentCheck

from six import iteritems

try:
    import pymqi
except ImportError:
    pymqi = None

from . import errors, metrics
from .config import IBMMQConfig
from .connection import get_queue_manager_connection


class IbmMqCheck(AgentCheck):

    METRIC_PREFIX = 'ibm_mq'

    SERVICE_CHECK = 'ibm_mq.can_connect'

    QUEUE_MANAGER_SERVICE_CHECK = 'ibm_mq.queue_manager'
    QUEUE_SERVICE_CHECK = 'ibm_mq.queue'

    def check(self, instance):
        if not pymqi:
            self.log.error("You need to install pymqi")
            raise errors.PymqiException("You need to install pymqi")

        config = IBMMQConfig(instance)

        config.check_properly_configured()

        try:
            queue_manager = get_queue_manager_connection(config)
            self.service_check(self.SERVICE_CHECK, AgentCheck.OK, config.tags)
        except Exception as e:
            self.warning("cannot connect to queue manager: {}".format(e))
            self.service_check(self.SERVICE_CHECK, AgentCheck.CRITICAL, config.tags)
            return

        self.queue_manager_stats(queue_manager, config.tags)
        self.channel_stats(queue_manager, config.tags)

        for queue_name in config.queues:
            queue_tags = config.tags + ["queue:{}".format(queue_name)]
            try:
                queue = pymqi.Queue(queue_manager, queue_name)
                self.queue_stats(queue, queue_tags)
                self.service_check(self.QUEUE_SERVICE_CHECK, AgentCheck.OK, queue_tags)
            except Exception as e:
                self.warning('Cannot connect to queue {}: {}'.format(queue_name, e))
                self.service_check(self.QUEUE_SERVICE_CHECK, AgentCheck.CRITICAL, queue_tags)

    def queue_manager_stats(self, queue_manager, tags):
        for mname, pymqi_value in iteritems(metrics.QUEUE_MANAGER_METRICS):
            try:
                m = queue_manager.inquire(pymqi_value)

                mname = '{}.queue_manager.{}'.format(self.METRIC_PREFIX, mname)
                self.gauge(mname, m, tags=tags)
                self.service_check(self.QUEUE_MANAGER_SERVICE_CHECK, AgentCheck.OK, tags)
            except pymqi.Error as e:
                self.warning("Error getting queue manager stats: {}".format(e))
                self.service_check(self.QUEUE_MANAGER_SERVICE_CHECK, AgentCheck.CRITICAL, tags)

    def queue_stats(self, queue, tags):
        for mname, pymqi_value in iteritems(metrics.QUEUE_METRICS):
            try:
                m = queue.inquire(pymqi_value)
                mname = '{}.queue.{}'.format(self.METRIC_PREFIX, mname)
                self.log.debug("name={} value={} tags={}".format(mname, m, tags))
                self.gauge(mname, m, tags=tags)
            except pymqi.Error as e:
                self.warning("Error getting queue stats: {}".format(e))

        for mname, func in iteritems(metrics.QUEUE_METRICS_FUNCTIONS):
            try:
                m = func(queue)
                mname = '{}.queue.{}'.format(self.METRIC_PREFIX, mname)
                self.log.debug("name={} value={} tags={}".format(mname, m, tags))
                self.gauge(mname, m, tags=tags)
            except pymqi.Error as e:
                self.warning("Error getting queue stats: {}".format(e))

    def channel_stats(self, queue_manager, tags):
        for mname, pymqi_value in iteritems(metrics.CHANNEL_METRICS):
            try:
                m = queue_manager.inquire(pymqi_value)
                mname = '{}.channel.{}'.format(self.METRIC_PREFIX, mname)
                self.log.debug("name={} value={} tags={}".format(mname, m, tags))
                self.gauge(mname, m, tags=tags)
            except pymqi.Error as e:
                self.warning("Error getting channel stats: {}".format(e))
