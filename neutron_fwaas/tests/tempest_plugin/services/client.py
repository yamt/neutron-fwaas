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

import time
import urllib


from oslo_serialization import jsonutils as json
from six.moves.urllib import parse
from tempest_lib.common.utils import misc
from tempest_lib import exceptions as lib_exc

from tempest.common import service_client
from tempest import exceptions


class _NeutronClientBase(service_client.ServiceClient):
    version = '2.0'
    uri_prefix = "v2.0"

    def get_uri(self, plural_name):
        # get service prefix from resource name
        service_prefix = self.service_resource_prefix_map.get(
            plural_name)
        if plural_name not in self.hyphen_exceptions:
            plural_name = plural_name.replace("_", "-")
        if service_prefix:
            uri = '%s/%s/%s' % (self.uri_prefix, service_prefix,
                                plural_name)
        else:
            uri = '%s/%s' % (self.uri_prefix, plural_name)
        return uri

    def pluralize(self, resource_name):
        # get plural from map or just add 's'
        return self.resource_plural_map.get(resource_name, resource_name + 's')

    def _lister(self, plural_name):
        def _list(**filters):
            uri = self.get_uri(plural_name)
            if filters:
                uri += '?' + parse.urlencode(filters, doseq=1)
            resp, body = self.get(uri)
            result = {plural_name: self.deserialize_list(body)}
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, result)

        return _list

    def _deleter(self, resource_name):
        def _delete(resource_id):
            plural = self.pluralize(resource_name)
            uri = '%s/%s' % (self.get_uri(plural), resource_id)
            resp, body = self.delete(uri)
            self.expected_success(204, resp.status)
            return service_client.ResponseBody(resp, body)

        return _delete

    def _shower(self, resource_name):
        def _show(resource_id, **fields):
            # fields is a dict which key is 'fields' and value is a
            # list of field's name. An example:
            # {'fields': ['id', 'name']}
            plural = self.pluralize(resource_name)
            uri = '%s/%s' % (self.get_uri(plural), resource_id)
            if fields:
                uri += '?' + parse.urlencode(fields, doseq=1)
            resp, body = self.get(uri)
            body = self.deserialize_single(body)
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, body)

        return _show

    def _creater(self, resource_name):
        def _create(**kwargs):
            plural = self.pluralize(resource_name)
            uri = self.get_uri(plural)
            post_data = self.serialize({resource_name: kwargs})
            resp, body = self.post(uri, post_data)
            body = self.deserialize_single(body)
            self.expected_success(201, resp.status)
            return service_client.ResponseBody(resp, body)

        return _create

    def _updater(self, resource_name):
        def _update(res_id, **kwargs):
            plural = self.pluralize(resource_name)
            uri = '%s/%s' % (self.get_uri(plural), res_id)
            post_data = self.serialize({resource_name: kwargs})
            resp, body = self.put(uri, post_data)
            body = self.deserialize_single(body)
            self.expected_success(200, resp.status)
            return service_client.ResponseBody(resp, body)

        return _update

    def __getattr__(self, name):
        method_prefixes = ["list_", "delete_", "show_", "create_", "update_"]
        method_functors = [self._lister,
                           self._deleter,
                           self._shower,
                           self._creater,
                           self._updater]
        for index, prefix in enumerate(method_prefixes):
            prefix_len = len(prefix)
            if name[:prefix_len] == prefix:
                return method_functors[index](name[prefix_len:])
        raise AttributeError(name)


class NeutronFWaaSClient(_NeutronClientBase):
    """
    Tempest REST client for Neutron FWaaS.
    """

    # The following list represents resource names that do not require
    # changing underscore to a hyphen
    hyphen_exceptions = [
        "firewall_rules",
        "firewall_policies",
    ]

    # the following map is used to construct proper URI
    # for the given neutron resource
    service_resource_prefix_map = {
        'firewall_rules': 'fw',
        'firewall_policies': 'fw',
        'firewalls': 'fw',
    }

    # map from resource name to a plural name
    # needed only for those which can't be constructed as name + 's'
    resource_plural_map = {
        'firewall_policy': 'firewall_policies',
    }

    def insert_firewall_rule_in_policy(self, firewall_policy_id,
                                       firewall_rule_id, insert_after="",
                                       insert_before=""):
        uri = '%s/fw/firewall_policies/%s/insert_rule' % (self.uri_prefix,
                                                          firewall_policy_id)
        body = {
            "firewall_rule_id": firewall_rule_id,
            "insert_after": insert_after,
            "insert_before": insert_before
        }
        body = json.dumps(body)
        resp, body = self.put(uri, body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)

    def remove_firewall_rule_from_policy(self, firewall_policy_id,
                                         firewall_rule_id):
        uri = '%s/fw/firewall_policies/%s/remove_rule' % (self.uri_prefix,
                                                          firewall_policy_id)
        update_body = {"firewall_rule_id": firewall_rule_id}
        update_body = json.dumps(update_body)
        resp, body = self.put(uri, update_body)
        self.expected_success(200, resp.status)
        body = json.loads(body)
        return service_client.ResponseBody(resp, body)
