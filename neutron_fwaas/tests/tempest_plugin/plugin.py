
import os
import sys

from tempest.test_discover import plugins


class NeutronFWaaSPlugin(plugins.TempestPlugin):
    def get_opt_lists(self):
        return []

    def load_tests(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        # top_level_dir = $(this_dir)/../../..
        d = os.path.split(this_dir)[0]
        d = os.path.split(d)[0]
        top_level_dir = os.path.split(d)[0]
        test_dir = os.path.join(top_level_dir,
            'neutron_fwaas/tests/tempest_plugin/tests/scenario')
        return (test_dir, top_level_dir)

    def register_opts(self):
        return
