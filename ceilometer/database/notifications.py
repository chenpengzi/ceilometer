#
# Copyright 2017 Eayun, Inc.
#
# Author: Eoghan Glynn <eglynn@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Handler for producing database metering messages from trove notification
   events.
"""
import copy

from oslo.config import cfg
import oslo.messaging

from ceilometer import plugin
from ceilometer import sample

cfg.CONF.import_opt('trove_control_exchange',
                    'ceilometer.profiler.notifications')


class DataBaseNotificationBase(plugin.NotificationBase):
    """Base class for database counting."""

    resource_name = None
    sample_type = None
    unit = None

    @property
    def event_types(self):
        return ['trove_database.meter']

    @staticmethod
    def get_targets(conf):
        """Return a sequence of oslo.messaging.Target

        This sequence is defining the exchange and topics to be connected for
        this plugin.
        """
        return [oslo.messaging.Target(topic=topic,
                                      exchange=conf.trove_control_exchange)
                for topic in conf.notification_topics]

    def process_notification(self, message):
        counter_name = getattr(self, 'counter_name', self.resource_name)
        counters = message['payload']['counter']
        resource_message = copy.deepcopy(message)
        del resource_message['payload']['counter']

        if counter_name in counters:
            new_name = '_'.join(counter_name.split('.'))
            resource_message['payload'].update(
                {new_name: counters[counter_name]})
            yield sample.Sample.from_notification(
                name=counter_name,
                type=self.sample_type,
                volume=message['payload']['counter'].get(counter_name),
                unit=self.unit,
                user_id=None,
                project_id=message['payload']['tenant_id'],
                resource_id=message['payload']['resource_id'],
                message=resource_message)
