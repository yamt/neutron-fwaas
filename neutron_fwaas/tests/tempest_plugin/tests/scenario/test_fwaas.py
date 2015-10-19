# Copyright (c) 2015 Midokura SARL
# All Rights Reserved.
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

import six
from tempest_lib.common.utils import data_utils
from tempest_lib import exceptions as lib_exc

from tempest import config
from tempest.scenario import manager
from tempest import test

from neutron_fwaas.tests.tempest_plugin.tests.scenario import base

CONF = config.CONF


class TestFWaaS(base.FWaaSScenarioTest):

    @classmethod
    def resource_setup(cls):
        super(TestFWaaS, cls).resource_setup()
        if not test.is_extension_enabled('fwaas', 'network'):
            msg = "FWaaS Extension not enabled."
            raise cls.skipException(msg)

    def _create_server(self, network):
        keys = self.create_keypair()
        kwargs = {
            'networks': [
                {'uuid': network['id']},
            ],
            'key_name': keys['name'],
            'security_groups': [
                {'name': self.security_group['name']},
            ]
        }
        server = self.create_server(create_kwargs=kwargs)
        return server, keys

    def _server_ip(self, server, network):
        return server['addresses'][network['name']][0]['addr']

    @test.idempotent_id('f970f6b3-6541-47ac-a9ea-f769be1e21a8')
    def test_firewall(self):
#        fw_rule = self.create_firewall_rule(protocol="tcp", action="allow")
#        fw_policy = self.create_firewall_policy(firewall_rules=[fw_rule['id']])

        self.security_group = self._create_security_group()
        network1, subnet1, router1 = self.create_networks()
        network2, subnet2, router2 = self.create_networks()
        self.assertEqual(router1['external_gateway_info']['network_id'],
                         router2['external_gateway_info']['network_id'])

        server1, keys1 = self._create_server(network1)
        public_network_id = CONF.network.public_network_id
        server2, keys2 = self._create_server(network2)
        floating_ip = self.create_floating_ip(server1, public_network_id)
        # server1_ip = self._server_ip(server1, network1)
        server1_ip = floating_ip.floating_ip_address
        access_point = self._ssh_to_server(server1_ip, keys1['private_key'])
        #self.assertEqual([], server2)
        self._check_remote_connectivity(access_point, ip, True)
