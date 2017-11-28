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


class MysqlTotalConnectPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.total.connections'
    unit = 'connect'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlThreadsConnectPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.threads.connections'
    unit = 'connect'
    sample_type = sample.TYPE_DELTA


class MysqlQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class MysqlTPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.tps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlTPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.tps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA


class MysqlSlowQueriesPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.slow.queries'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlSyncSlaveDelayPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.sync.delay'
    unit = 's'
    sample_type = sample.TYPE_DELTA


class MysqlScanFullTablePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.scan.full.table'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlBufferPoolDirtyRatioPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.buffer.pool.dirty.ratio'
    unit = '%'
    sample_type = sample.TYPE_DELTA


class MysqlBufferPoolSizePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.buffer.pool.size'
    unit = 'MB'
    sample_type = sample.TYPE_GAUGE


class MysqlBufferPoolReadHitsRatioPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.buffer.pool.read.hits.ratio'
    unit = '%'
    sample_type = sample.TYPE_DELTA


class MysqlQcacheQueryHitsRatioPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.qcache.query.hits.ratio'
    unit = '%'
    sample_type = sample.TYPE_DELTA


class MysqlCachedConnectionsHitsRatioPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.cached.connections.hits.ratio'
    unit = '%'
    sample_type = sample.TYPE_DELTA


class MysqlThreadsRunningPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.threads.running'
    unit = 'connect'
    sample_type = sample.TYPE_DELTA


class MysqlMaxConnectionsPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.max.connections'
    unit = 'connect'
    sample_type = sample.TYPE_GAUGE


class MysqlTransactionCommitPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.transaction.commit'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlTransactionRollbackPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.transaction.rollback'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlTotalSelectPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.total.select'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlReplaceQPSPollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.replace.qps'
    unit = 'request'
    sample_type = sample.TYPE_CUMULATIVE


class MysqlReplaceQPSRatePollster(DataBaseNotificationBase):
    """Listen for Trove notifications.
       Listen in order to mediate with the metering framework.
    """
    resource_name = 'mysql.replace.qps.rate'
    unit = 'request/s'
    sample_type = sample.TYPE_DELTA
