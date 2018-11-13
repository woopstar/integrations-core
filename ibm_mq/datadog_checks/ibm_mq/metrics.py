# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

class Metrics:
    def __init__(self):
        import pymqi
        self.pymqi = pymqi

    def queue_metrics(self):
        return {
            'service_interval': self.pymqi.CMQC.MQIA_Q_SERVICE_INTERVAL,
            'inhibit_put': self.pymqi.CMQC.MQIA_INHIBIT_PUT,
            'depth_low_limit': self.pymqi.CMQC.MQIA_Q_DEPTH_LOW_LIMIT,
            'inhibit_get': self.pymqi.CMQC.MQIA_INHIBIT_GET,
            'harden_get_backout': self.pymqi.CMQC.MQIA_HARDEN_GET_BACKOUT,
            'service_interval_event': self.pymqi.CMQC.MQIA_Q_SERVICE_INTERVAL_EVENT,
            'trigger_control': self.pymqi.CMQC.MQIA_TRIGGER_CONTROL,
            'usage': self.pymqi.CMQC.MQIA_USAGE,
            'scope': self.pymqi.CMQC.MQIA_SCOPE,
            'type': self.pymqi.CMQC.MQIA_Q_TYPE,
            'depth_max': self.pymqi.CMQC.MQIA_MAX_Q_DEPTH,
            'backout_threshold': self.pymqi.CMQC.MQIA_BACKOUT_THRESHOLD,
            'depth_high_event': self.pymqi.CMQC.MQIA_Q_DEPTH_HIGH_EVENT,
            'depth_low_event': self.pymqi.CMQC.MQIA_Q_DEPTH_LOW_EVENT,
            'trigger_message_priority': self.pymqi.CMQC.MQIA_TRIGGER_MSG_PRIORITY,
            'depth_current': self.pymqi.CMQC.MQIA_CURRENT_Q_DEPTH,
            'depth_max_event': self.pymqi.CMQC.MQIA_Q_DEPTH_MAX_EVENT,
            'open_input_count': self.pymqi.CMQC.MQIA_OPEN_INPUT_COUNT,
            'persistence': self.pymqi.CMQC.MQIA_DEF_PERSISTENCE,
            'trigger_depth': self.pymqi.CMQC.MQIA_TRIGGER_DEPTH,
            'max_message_length': self.pymqi.CMQC.MQIA_MAX_MSG_LENGTH,
            'depth_high_limit': self.pymqi.CMQC.MQIA_Q_DEPTH_HIGH_LIMIT,
            'priority': self.pymqi.CMQC.MQIA_DEF_PRIORITY,
            'input_open_option': self.pymqi.CMQC.MQIA_DEF_INPUT_OPEN_OPTION,
            'message_delivery_sequence': self.pymqi.CMQC.MQIA_MSG_DELIVERY_SEQUENCE,
            'retention_interval': self.pymqi.CMQC.MQIA_RETENTION_INTERVAL,
            'open_output_count': self.pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT,
            'trigger_type': self.pymqi.CMQC.MQIA_TRIGGER_TYPE,
            'max_channels': self.pymqi.CMQC.MQIA_MAX_CHANNELS
        }

    def queue_manager_metrics(self):
        return {
            'dist_lists': self.pymqi.CMQC.MQIA_DIST_LISTS,
            'max_msg_list': self.pymqi.CMQC.MQIA_MAX_MSG_LENGTH,
        }

    def channel_metrics(self):
        return {
            'batch_size': self.pymqi.CMQCFC.MQIACH_BATCH_SIZE,
            'batch_interval': self.pymqi.CMQCFC.MQIACH_BATCH_INTERVAL,
            'long_retry_count': self.pymqi.CMQCFC.MQIACH_LONG_RETRY,
            'long_retry_interval': self.pymqi.CMQCFC.MQIACH_LONG_TIMER,
            'max_message_length': self.pymqi.CMQCFC.MQIACH_MAX_MSG_LENGTH,
            'short_retry_count': self.pymqi.CMQCFC.MQIACH_SHORT_RETRY,
        }

    def depth_percent(self, queue):
        depth_current = queue.inquire(self.queue_metrics()['depth_current'])
        depth_max = queue.inquire(self.queue_metrics()['depth_max'])

        depth_fraction = depth_current / depth_max
        depth_percent = depth_fraction * 100

        return depth_percent

    def queue_metrics_functions(self):
        return {
            'depth_percent': self.depth_percent,
        }
