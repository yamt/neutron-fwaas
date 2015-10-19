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

    @test.idempotent_id('94d8faf5e74ff28f3f64fcc1d0ea201b4ba1ba2d')
    def test_firewall(self):
        fw_rule = self.create_firewall_rule(protocol="tcp", action="allow")
        fw_policy = self.create_firewall_policy(firewall_rules=[fw_rule['id']])

        network1, subnet1, router1 = self.create_networks()
        network2, subnet2, router2 = self.create_networks()
        self.aasertEqual(router1, router2)

        access_point = self._ssh_to_server(server, key)
        self._check_remote_connectivity(access_point, ip, should_succeed)
