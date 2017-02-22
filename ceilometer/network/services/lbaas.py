#
# Copyright 2014 Cisco Systems,Inc.
#
# Author: Pradeep Kilambi <pkilambi@cisco.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import abc
import collections
import os.path
import socket

from oslo.utils import timeutils
import six

from ceilometer.network.services import base
from ceilometer.openstack.common.gettextutils import _
from ceilometer.openstack.common import log
from ceilometer import sample

LOG = log.getLogger(__name__)

LBStatsData = collections.namedtuple(
    'LBStats',
    ['active_connections', 'total_connections', 'bytes_in', 'bytes_out']
)


class LBPoolPollster(base.BaseServicesPollster):
    """Pollster to capture Load Balancer pool status samples."""

    FIELDS = ['admin_state_up',
              'description',
              'lb_method',
              'name',
              'protocol',
              'provider',
              'status',
              'status_description',
              'subnet_id',
              'vip_id'
              ]

    @property
    def default_discovery(self):
        return 'lb_pools'

    def get_samples(self, manager, cache, resources):
        resources = resources or []

        for pool in resources:
            LOG.debug("Load Balancer Pool : %s" % pool)
            status = self.get_status_id(pool['status'])
            if status == -1:
                # unknown status, skip this sample
                LOG.warn(_("Unknown status %(stat)s received on pool %(id)s, "
                           "skipping sample") % {'stat': pool['status'],
                                                 'id': pool['id']})
                continue

            yield sample.Sample(
                name='network.services.lb.pool',
                type=sample.TYPE_GAUGE,
                unit='pool',
                volume=status,
                user_id=None,
                project_id=pool['tenant_id'],
                resource_id=pool['id'],
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata=self.extract_metadata(pool)
            )


class LBVipPollster(base.BaseServicesPollster):
    """Pollster to capture Load Balancer Vip status samples."""

    FIELDS = ['admin_state_up',
              'address',
              'connection_limit',
              'description',
              'name',
              'pool_id',
              'port_id',
              'protocol',
              'protocol_port',
              'status',
              'status_description',
              'subnet_id',
              'session_persistence',
              ]

    @property
    def default_discovery(self):
        return 'lb_vips'

    def get_samples(self, manager, cache, resources):
        resources = resources or []

        for vip in resources:
            LOG.debug("Load Balancer Vip : %s" % vip)
            status = self.get_status_id(vip['status'])
            if status == -1:
                # unknown status, skip this sample
                LOG.warn(_("Unknown status %(stat)s received on vip %(id)s, "
                         "skipping sample") % {'stat': vip['status'],
                                               'id': vip['id']})
                continue

            yield sample.Sample(
                name='network.services.lb.vip',
                type=sample.TYPE_GAUGE,
                unit='vip',
                volume=status,
                user_id=None,
                project_id=vip['tenant_id'],
                resource_id=vip['id'],
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata=self.extract_metadata(vip)
            )


class LBMemberPollster(base.BaseServicesPollster):
    """Pollster to capture Load Balancer Member status samples."""

    FIELDS = ['admin_state_up',
              'address',
              'pool_id',
              'protocol_port',
              'status',
              'status_description',
              'weight',
              ]

    @property
    def default_discovery(self):
        return 'lb_members'

    def get_samples(self, manager, cache, resources):
        resources = resources or []

        for member in resources:
            LOG.debug("Load Balancer Member : %s" % member)
            status = self.get_status_id(member['status'])
            if status == -1:
                LOG.warn(_("Unknown status %(stat)s received on member %(id)s,"
                         "skipping sample") % {'stat': member['status'],
                                               'id': member['id']})
                continue
            yield sample.Sample(
                name='network.services.lb.member',
                type=sample.TYPE_GAUGE,
                unit='member',
                volume=status,
                user_id=None,
                project_id=member['tenant_id'],
                resource_id=member['id'],
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata=self.extract_metadata(member)
            )


class LBHealthMonitorPollster(base.BaseServicesPollster):
    """Pollster to capture Load Balancer Health probes status samples."""

    FIELDS = ['admin_state_up',
              'delay',
              'max_retries',
              'pools',
              'timeout',
              'type'
              ]

    @property
    def default_discovery(self):
        return 'lb_health_probes'

    def get_samples(self, manager, cache, resources):
        for probe in resources:
            LOG.debug("Load Balancer Health probe : %s" % probe)
            yield sample.Sample(
                name='network.services.lb.health_monitor',
                type=sample.TYPE_GAUGE,
                unit='monitor',
                volume=1,
                user_id=None,
                project_id=probe['tenant_id'],
                resource_id=probe['id'],
                timestamp=timeutils.utcnow().isoformat(),
                resource_metadata=self.extract_metadata(probe)
            )


@six.add_metaclass(abc.ABCMeta)
class _LBStatsPollster(base.BaseServicesPollster):
    """Base Statistics pollster.

     It is capturing the statistics info and yielding samples for connections
     and bandwidth.
    """

    def _get_lb_pools(self):
        return self.nc.pool_get_all()

    def _get_pool_stats(self, pool_id):
        return self.nc.pool_stats(pool_id)

    @staticmethod
    def make_sample_from_pool(pool, name, type, unit, volume,
                              resource_metadata=None):
        if not resource_metadata:
            resource_metadata = {}
        return sample.Sample(
            name=name,
            type=type,
            unit=unit,
            volume=volume,
            user_id=None,
            project_id=pool['tenant_id'],
            resource_id=pool['id'],
            timestamp=timeutils.isotime(),
            resource_metadata=resource_metadata,
        )

    def _populate_stats_cache(self, pool_id, cache):
        i_cache = cache.setdefault("lbstats", {})
        if pool_id not in i_cache:
            stats = self._get_pool_stats(pool_id)['stats']
            i_cache[pool_id] = LBStatsData(
                active_connections=stats['active_connections'],
                total_connections=stats['total_connections'],
                bytes_in=stats['bytes_in'],
                bytes_out=stats['bytes_out'],
            )
        return i_cache[pool_id]

    @property
    def default_discovery(self):
        return 'lb_pools'

    @abc.abstractmethod
    def _get_sample(pool, c_data):
        """Return one Sample."""

    def get_samples(self, manager, cache, resources):
        for pool in resources:
            try:
                c_data = self._populate_stats_cache(pool['id'], cache)
                yield self._get_sample(pool, c_data)
            except Exception as err:
                LOG.exception(_('Ignoring pool %(pool_id)s: %(error)s'),
                              {'pool_id': pool['id'], 'error': err})


class LBActiveConnectionsPollster(_LBStatsPollster):
    """Pollster to capture Active Load Balancer connections."""

    @staticmethod
    def _get_sample(pool, data):
        return make_sample_from_pool(
            pool,
            name='network.services.lb.active.connections',
            type=sample.TYPE_GAUGE,
            unit='connection',
            volume=data.active_connections,
        )


class LBTotalConnectionsPollster(_LBStatsPollster):
    """Pollster to capture Total Load Balancer connections."""

    @staticmethod
    def _get_sample(pool, data):
        return make_sample_from_pool(
            pool,
            name='network.services.lb.total.connections',
            type=sample.TYPE_GAUGE,
            unit='connection',
            volume=data.total_connections,
        )


class LBBytesInPollster(_LBStatsPollster):
    """Pollster to capture incoming bytes."""

    @staticmethod
    def _get_sample(pool, data):
        return make_sample_from_pool(
            pool,
            name='network.services.lb.incoming.bytes',
            type=sample.TYPE_CUMULATIVE,
            unit='B',
            volume=data.bytes_in,
        )


class LBBytesOutPollster(_LBStatsPollster):
    """Pollster to capture outgoing bytes."""

    @staticmethod
    def _get_sample(pool, data):
        return make_sample_from_pool(
            pool,
            name='network.services.lb.outgoing.bytes',
            type=sample.TYPE_CUMULATIVE,
            unit='B',
            volume=data.bytes_out,
        )


def make_sample_from_pool(pool, name, type, unit, volume,
                          resource_metadata=None):
    resource_metadata = resource_metadata or {}

    return sample.Sample(
        name=name,
        type=type,
        unit=unit,
        volume=volume,
        user_id=None,
        project_id=pool['tenant_id'],
        resource_id=pool['id'],
        timestamp=timeutils.isotime(),
        resource_metadata=resource_metadata,
    )


class _ESLBStatsPollster(base.BaseServicesPollster):

    FIELDS = ['id',
              'name',
              'protocol',
              'members',
              'vip_id'
              ]

    def _get_stats_from_socket(self, socket_path, entity_type):
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(socket_path)
            s.send('show stat -1 %s -1\n' % entity_type)
            raw_stats = ''
            chunk_size = 1024
            while True:
                chunk = s.recv(chunk_size)
                raw_stats += chunk
                if len(chunk) < chunk_size:
                    break
        except socket.error:
            return []

        stat_lines = raw_stats.splitlines()
        if len(stat_lines) < 2:
            return []
        stat_names = [name.strip('# ') for name in stat_lines[0].split(',')]
        res_stats = []
        for raw_values in stat_lines[1:]:
            if not raw_values:
                continue
            stat_values = [
                value.strip() for value in raw_values.split(',')]
            res_stats.append(dict(zip(stat_names, stat_values)))

        return res_stats

    def _get_pool_stats(self, pool_id, protocol):
        TYPE_FRONTEND_REQUEST = 1
        TYPE_SERVER_REQUEST = 4
        TYPE_FRONTEND_RESPONSE = '0'
        TYPE_SERVER_RESPONSE = '2'
        POOL_PROTOCOL_TCP = 'TCP'
        STAT_KEYS = ['bin', 'bout', 'stot']
        STAT_KEYS_HTTP_ONLY = [
            'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx', 'hrsp_5xx',
            'req_tot',  # frontend only
            'rtime'  # server only
        ]

        ret = []
        stat_keys = STAT_KEYS
        if protocol != POOL_PROTOCOL_TCP:
            stat_keys += STAT_KEYS_HTTP_ONLY

        socket_path = "/var/lib/neutron/lbaas/%s/sock" % pool_id
        if os.path.exists(socket_path):
            stats = self._get_stats_from_socket(
                socket_path,
                entity_type=TYPE_FRONTEND_REQUEST | TYPE_SERVER_REQUEST)
            for stat in stats:
                to_ignore = set()
                resource_stat = {}
                if stat['type'] == TYPE_FRONTEND_RESPONSE:
                    resource_id = stat['pxname']
                    to_ignore.add('rtime')
                elif stat['type'] == TYPE_SERVER_RESPONSE:
                    resource_id = stat['svname']
                    to_ignore.add('req_tot')
                    # Report server uptime/downtime
                    if stat['status'] == 'UP':
                        resource_stat['uptime'] = stat['lastchg']
                    elif stat['status'] == 'DOWN':
                        resource_stat['downtime'] = stat['lastchg']
                resource_stat['resource_id'] = resource_id
                for key in stat_keys:
                    if key not in to_ignore:
                        resource_stat[key] = stat.get(key, 0)
                ret.append(resource_stat)

        return ret

    def _populate_stats_cache(self, pool_id, protocol, cache):
        i_cache = cache.setdefault("lbstats", {})
        if pool_id not in i_cache:
            i_cache[pool_id] = self._get_pool_stats(pool_id, protocol)
        return i_cache[pool_id]

    @property
    def default_discovery(self):
        return 'lb_hosted_haproxy_pools'

    def get_samples(self, manager, cache, resources):
        for pool in resources:
            tenant_id = pool['tenant_id']
            pool_id = pool['id']
            try:
                stats = self._populate_stats_cache(pool_id, pool['protocol'],
                                                   cache)
                for stat in stats:
                    if self.stat_key in stat:
                        yield sample.Sample(
                            name=self.name,
                            type=self.sample_type,
                            unit=self.unit,
                            volume=stat[self.stat_key],
                            user_id=None,
                            project_id=tenant_id,
                            resource_id=stat['resource_id'],
                            timestamp=timeutils.utcnow().isoformat(),
                            resource_metadata=self.extract_metadata(pool)
                        )
            except Exception as err:
                LOG.exception(_('Ignoring pool %(pool_id)s: %(error)s'),
                              {'pool_id': pool_id, 'error': err})


class ESLBBytesInPollster(_ESLBStatsPollster):
    stat_key = 'bin'
    name = 'network.services.es.lb.incoming.bytes'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'B'


class ESLBBytesOutPollster(_ESLBStatsPollster):
    stat_key = 'bout'
    name = 'network.services.es.lb.outgoing.bytes'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'B'


class ESLBTotalConnectionsPollster(_ESLBStatsPollster):
    stat_key = 'stot'
    name = 'network.services.es.lb.total.connections'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'connection'


class ESLBServerUptimePollster(_ESLBStatsPollster):
    stat_key = 'uptime'
    name = 'network.services.es.lb.server.uptime'
    sample_type = sample.TYPE_GAUGE
    unit = 's'


class ESLBServerDowntimePollster(_ESLBStatsPollster):
    stat_key = 'downtime'
    name = 'network.services.es.lb.server.downtime'
    sample_type = sample.TYPE_GAUGE
    unit = 's'


class ESLBTotalHTTPRequestsPollster(_ESLBStatsPollster):
    stat_key = 'req_tot'
    name = 'network.services.es.lb.http.requests'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'request'


class ESLBAverageHTTPResponseTimePollster(_ESLBStatsPollster):
    stat_key = 'rtime'
    name = 'network.services.es.lb.http.response.time'
    sample_type = sample.TYPE_GAUGE
    unit = 'ms'


class ESLBHTTP1xxResponsesPollster(_ESLBStatsPollster):
    stat_key = 'hrsp_1xx'
    name = 'network.services.es.lb.http.response.1xx'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'response'


class ESLBHTTP2xxResponsesPollster(_ESLBStatsPollster):
    stat_key = 'hrsp_2xx'
    name = 'network.services.es.lb.http.response.2xx'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'response'


class ESLBHTTP3xxResponsesPollster(_ESLBStatsPollster):
    stat_key = 'hrsp_3xx'
    name = 'network.services.es.lb.http.response.3xx'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'response'


class ESLBHTTP4xxResponsesPollster(_ESLBStatsPollster):
    stat_key = 'hrsp_4xx'
    name = 'network.services.es.lb.http.response.4xx'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'response'


class ESLBHTTP5xxResponsesPollster(_ESLBStatsPollster):
    stat_key = 'hrsp_5xx'
    name = 'network.services.es.lb.http.response.5xx'
    sample_type = sample.TYPE_CUMULATIVE
    unit = 'response'
