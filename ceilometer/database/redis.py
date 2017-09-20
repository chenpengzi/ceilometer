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


class RedisMemoryUsagePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.memory.usage'
    unit = '%'
    sample_type = sample.TYPE_DELTA


class RedisQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisTotalRecConnPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.total.received.connections'
    unit = 'connect'
    sample_type = sample.TYPE_CUMULATIVE


class RedisClientsConnectionsPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.clients.connections'
    unit = 'connect'
    sample_type = sample.TYPE_DELTA


class RedisTotalKeysPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.total.keys'
    unit = 'key'
    sample_type = sample.TYPE_DELTA


class RedisExpiredKeysPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.expire.keys'
    unit = 'key'
    sample_type = sample.TYPE_CUMULATIVE


class RedisEvictedKeysPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.evicte.keys'
    unit = 'key'
    sample_type = sample.TYPE_CUMULATIVE


class RedisKeyspaceHitsPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.keyspace.hits'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisKeyspaceHitsRatioPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.keyspace.hits.ratio'
    unit = '%'
    sample_type = sample.TYPE_DELTA


class RedisSetQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.set.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisSetQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.set.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisListQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.list.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisListQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.list.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisStringQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.string.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisStringQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.string.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisHashQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.hash.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisHashQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.hash.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisZsetQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.zset.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisZsetQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.zset.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisHyperLoglogQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.hyperloglog.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisHyperLoglogQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.hyperloglog.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisPubsubQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.pubsub.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisPubsubQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.pubsub.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class RedisTransactionQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.transaction.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class RedisTransactionQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'redis.transaction.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA
