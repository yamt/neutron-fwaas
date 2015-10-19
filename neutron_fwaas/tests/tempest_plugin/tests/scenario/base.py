
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
        cls.fwaas_client = client.NeutronFWaaSClient(
            self.auth_provider,
            CONF.network.catalog_type,
            CONF.network.region or CONF.identity.region,
            endpoint_type=CONF.network.endpoint_type,
            build_interval=CONF.network.build_interval,
            build_timeout=CONF.network.build_timeout,
            **self.default_params)
        cls.fw_rules = []
        cls.fw_policies = []

    @classmethod
    def resource_cleanup(cls):
        if CONF.service_available.neutron:
            # Clean up firewall policies
            for fw_policy in cls.fw_policies:
                cls._try_delete_resource(cls.client.delete_firewall_policy,
                                         fw_policy['id'])
            # Clean up firewall rules
            for fw_rule in cls.fw_rules:
                cls._try_delete_resource(cls.client.delete_firewall_rule,
                                         fw_rule['id'])

    @classmethod
    def create_firewall_rule(cls, action, protocol):
        """Wrapper utility that returns a test firewall rule."""
        body = cls.client.create_firewall_rule(
            name=data_utils.rand_name("fw-rule"),
            action=action,
            protocol=protocol)
        fw_rule = body['firewall_rule']
        cls.fw_rules.append(fw_rule)
        return fw_rule

    @classmethod
    def create_firewall_policy(cls):
        """Wrapper utility that returns a test firewall policy."""
        body = cls.client.create_firewall_policy(
            name=data_utils.rand_name("fw-policy"))
        fw_policy = body['firewall_policy']
        cls.fw_policies.append(fw_policy)
        return fw_policy
