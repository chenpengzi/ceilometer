# Copyright 2016 Eayun, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from oslo.utils import timeutils

from ceilometer import plugin
from ceilometer import sample
from ceilometer import utils
from ceilometer.openstack.common import log
from ceilometer.openstack.common import processutils

LOG = log.getLogger(__name__)

IPT_CHAIN_NAME_LEN = 28


class _ESPortMeteringPollster(plugin.PollsterBase):

    @staticmethod
    def _get_ipt_chain_counters(chain):
        stats = {'packets': 0, 'bytes': 0}
        cmd = ['iptables', '-t', 'filter', '-L', chain,
               '-n', '-v', '-x', '-Z']
        try:
            (out, _) = utils.execute(*cmd, run_as_root=True)
        except processutils.ProcessExecutionError as err:
            LOG.error('Failed to get counters for iptables chain %(chain)s: '
                      '%(error)s', {'chain': chain, 'error': err})
            return stats

        lines = out.split('\n')
        for line in lines[2:]:
            if not line:
                break
            data = line.split()
            if (
                len(data) < 2 or
                not data[0].isdigit() or
                not data[1].isdigit()
            ):
                break
            stats['packets'] += int(data[0])
            stats['bytes'] += int(data[1])

        return stats

    def _get_port_stat(self, port_id):
        port_stat = {}
        for direction, key_prefix in (('ingress', 'in'), ('egress', 'out')):
            overall_chain = '-'.join(
                ['counting', direction, port_id])[:IPT_CHAIN_NAME_LEN]
            internal_chain = '-'.join(
                ['counting-in', direction, port_id])[:IPT_CHAIN_NAME_LEN]
            overall_stats = self._get_ipt_chain_counters(overall_chain)
            internal_stats = self._get_ipt_chain_counters(internal_chain)
            for counter in ('packets', 'bytes'):
                key_name = '_'.join([key_prefix, counter])
                in_key_name = '_'.join([key_prefix, 'internal', counter])
                ex_key_name = '_'.join([key_prefix, 'external', counter])
                all_s = port_stat[key_name] = overall_stats[counter]
                in_s = port_stat[in_key_name] = internal_stats[counter]
                port_stat[ex_key_name] = all_s - in_s if all_s > in_s else 0
        return port_stat

    def _populate_stats_cache(self, port_id, cache):
        i_cache = cache.setdefault("port_meter_stats", {})
        if port_id not in i_cache:
            i_cache[port_id] = self._get_port_stat(port_id)
        return i_cache[port_id]

    @property
    def default_discovery(self):
        return 'es_metering_ports'

    def get_samples(self, manager, cache, resources):
        for port in resources:
            tenant_id = port['tenant_id']
            port_id = port['id']
            try:
                port_stat = self._populate_stats_cache(port_id, cache)
                yield sample.Sample(
                    name=self.name,
                    type=self.sample_type,
                    unit=self.unit,
                    volume=port_stat[self.stat_key],
                    user_id=None,
                    project_id=tenant_id,
                    resource_id=port_id,
                    timestamp=timeutils.utcnow().isoformat(),
                    resource_metadata={})
            except Exception as err:
                LOG.exception('Ignoring port %(port_id)s: %(error)s',
                              {'port_id': port_id, 'error': err})


class ESPortBytesInPollster(_ESPortMeteringPollster):
    stat_key = 'in_bytes'
    name = 'network.es.port.incoming.bytes'
    sample_type = sample.TYPE_GAUGE
    unit = 'B'


class ESPortPacketsInPollster(_ESPortMeteringPollster):
    stat_key = 'in_packets'
    name = 'network.es.port.incoming.packets'
    sample_type = sample.TYPE_GAUGE
    unit = 'packet'


class ESPortInternalBytesInPollster(_ESPortMeteringPollster):
    stat_key = 'in_internal_bytes'
    name = 'network.es.port.incoming.internal.bytes'
    sample_type = sample.TYPE_GAUGE
    unit = 'B'


class ESPortInternalPacketsInPollster(_ESPortMeteringPollster):
    stat_key = 'in_internal_packets'
    name = 'network.es.port.incoming.internal.packets'
    sample_type = sample.TYPE_GAUGE
    unit = 'packet'


class ESPortExternalBytesInPollster(_ESPortMeteringPollster):
    stat_key = 'in_external_bytes'
    name = 'network.es.port.incoming.external.bytes'
    sample_type = sample.TYPE_GAUGE
    unit = 'B'


class ESPortExternalPacketsInPollster(_ESPortMeteringPollster):
    stat_key = 'in_external_packets'
    name = 'network.es.port.incoming.external.packets'
    sample_type = sample.TYPE_GAUGE
    unit = 'packet'


class ESPortBytesOutPollster(_ESPortMeteringPollster):
    stat_key = 'out_bytes'
    name = 'network.es.port.outgoing.bytes'
    sample_type = sample.TYPE_GAUGE
    unit = 'B'


class ESPortPacketsOutPollster(_ESPortMeteringPollster):
    stat_key = 'out_packets'
    name = 'network.es.port.outgoing.packets'
    sample_type = sample.TYPE_GAUGE
    unit = 'packet'


class ESPortInternalBytesOutPollster(_ESPortMeteringPollster):
    stat_key = 'out_internal_bytes'
    name = 'network.es.port.outgoing.internal.bytes'
    sample_type = sample.TYPE_GAUGE
    unit = 'B'


class ESPortInternalPacketsOutPollster(_ESPortMeteringPollster):
    stat_key = 'out_internal_packets'
    name = 'network.es.port.outgoing.internal.packets'
    sample_type = sample.TYPE_GAUGE
    unit = 'packet'


class ESPortExternalBytesOutPollster(_ESPortMeteringPollster):
    stat_key = 'out_external_bytes'
    name = 'network.es.port.outgoing.external.bytes'
    sample_type = sample.TYPE_GAUGE
    unit = 'B'


class ESPortExternalPacketsOutPollster(_ESPortMeteringPollster):
    stat_key = 'out_external_packets'
    name = 'network.es.port.outgoing.external.packets'
    sample_type = sample.TYPE_GAUGE
    unit = 'packet'
