#
# Copyright 2017 Eayun, Inc.
#
# Author: Julien Danjou <julien@danjou.info>
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

from ceilometer import sample
from notifications import DataBaseNotificationBase


class MongoMaxConnsPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.max.connections'
    unit = 'connect'
    sample_type = sample.TYPE_DELTA


class MongoConnectUseRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.connections.usage'
    unit = '%'
    sample_type = sample.TYPE_DELTA


class MongoQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MongoQPSRatePollster(DataBaseNotificationBase):
        """Listen for Trove notifications.
           Listen in order to mediate with the metering framework.
        """
        resource_name = 'mongo.qps.rate'
        unit = 'request/s'
        sample_type = sample.TYPE_DELTA


class MongoTotalRequestsPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.total.requests'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MongoInsertPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.insert.requests'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MongoQueryPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.query.requests'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MongoUpdatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.update.requests'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MongoDeletePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.delete.requests'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MongoGetMorePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.getmore.requests'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MongoCommandPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mongo.command.requests'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE
