
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

    @test.idempotent_id('1b84cf01-9c09-4ce7-bc72-b15e39076468')
    def test_firewall(self):
        fw_rule = self.create_firewall_rule("allow", "tcp")
        fw_policy = self.create_firewall_policy()
        network, subnet, router = self.create_networks()
        network, subnet, router = self.create_networks()
