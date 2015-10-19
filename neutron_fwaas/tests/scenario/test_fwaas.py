
import six
from tempest_lib.common.utils import data_utils
from tempest_lib import exceptions as lib_exc

from neutron.tests.api import base
from neutron.tests.tempest import config
from neutron.tests.tempest import exceptions
from neutron.tests.tempest import test

CONF = config.CONF


class TestFWaaS(base.BaseNetworkTest):

    @classmethod
    def resource_setup(cls):
        super(TestFWaaS, cls).resource_setup()
        if not test.is_extension_enabled('fwaas', 'network'):
            msg = "FWaaS Extension not enabled."
            raise cls.skipException(msg)
        cls.fw_rule = cls.create_firewall_rule("allow", "tcp")
        cls.fw_policy = cls.create_firewall_policy()

    def _try_delete_policy(self, policy_id):
        # delete policy, if it exists
        try:
            self.client.delete_firewall_policy(policy_id)
        # if policy is not found, this means it was deleted in the test
        except lib_exc.NotFound:
            pass

    def _try_delete_rule(self, rule_id):
        # delete rule, if it exists
        try:
            self.client.delete_firewall_rule(rule_id)
        # if rule is not found, this means it was deleted in the test
        except lib_exc.NotFound:
            pass

    def _try_delete_firewall(self, fw_id):
        # delete firewall, if it exists
        try:
            self.client.delete_firewall(fw_id)
        # if firewall is not found, this means it was deleted in the test
        except lib_exc.NotFound:
            pass

        self.client.wait_for_resource_deletion('firewall', fw_id)

    def _wait_until_ready(self, fw_id):
        target_states = ('ACTIVE', 'CREATED')

        def _wait():
            firewall = self.client.show_firewall(fw_id)
            firewall = firewall['firewall']
            return firewall['status'] in target_states

        if not test.call_until_true(_wait, CONF.network.build_timeout,
                                    CONF.network.build_interval):
            m = ("Timed out waiting for firewall %s to reach %s state(s)" %
                 (fw_id, target_states))
            raise exceptions.TimeoutException(m)

    @test.idempotent_id('1b84cf01-9c09-4ce7-bc72-b15e39076468')
    def test_firewall(self):
        network, subnet, router = self.create_networks()
        network, subnet, router = self.create_networks()
