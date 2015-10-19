
import six
from tempest_lib.common.utils import data_utils
from tempest_lib import exceptions as lib_exc

from tempest import config
from tempest.scenario import manager
from tempest import test

from neutron_fwaas.tests.tempest_plugin.services import client

CONF = config.CONF


class FWaaSScenarioTest(manager.NetworkScenarioTest):

    @classmethod
    def resource_setup(cls):
        super(FWaaSScenarioTest, cls).resource_setup()
        manager = cls.manager
        cls.firewalls_client = client.FirewallsClient(
            manager.auth_provider,
            CONF.network.catalog_type,
            CONF.network.region or CONF.identity.region,
            endpoint_type=CONF.network.endpoint_type,
            build_interval=CONF.network.build_interval,
            build_timeout=CONF.network.build_timeout,
            **manager.default_params)
        cls.firewall_policies_client = client.FirewallPoliciesClient(
            manager.auth_provider,
            CONF.network.catalog_type,
            CONF.network.region or CONF.identity.region,
            endpoint_type=CONF.network.endpoint_type,
            build_interval=CONF.network.build_interval,
            build_timeout=CONF.network.build_timeout,
            **manager.default_params)
        cls.firewall_rules_client = client.FirewallRulesClient(
            manager.auth_provider,
            CONF.network.catalog_type,
            CONF.network.region or CONF.identity.region,
            endpoint_type=CONF.network.endpoint_type,
            build_interval=CONF.network.build_interval,
            build_timeout=CONF.network.build_timeout,
            **manager.default_params)

    def create_firewall_rule(self, action, protocol):
        """Wrapper utility that returns a test firewall rule."""
        body = self.firewall_rules_client.create_firewall_rule(
            name=data_utils.rand_name("fw-rule"),
            action=action,
            protocol=protocol)
        fw_rule = body['firewall_rule']
        self.addCleanup(self.delete_wrapper,
                        self.firewall_rules_client.delete_firewall_rule,
                        fw_rule['id'])
        return fw_rule

    @classmethod
    def create_firewall_policy(cls):
        """Wrapper utility that returns a test firewall policy."""
        body = self.firewall_policies_client.create_firewall_policy(
            name=data_utils.rand_name("fw-policy"))
        fw_policy = body['firewall_policy']
        self.addCleanup(self.delete_wrapper,
                        self.firewall_firewalls_client.delete_firewall_policy,
                        fw_policy['id'])
        return fw_policy
