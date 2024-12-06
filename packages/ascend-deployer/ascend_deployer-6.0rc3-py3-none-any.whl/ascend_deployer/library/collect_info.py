#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ===========================================================================
import os
import platform

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.facts.collector import BaseFactCollector
from ansible.module_utils.common_info import get_npu_info, get_os_and_arch, parse_os_release, get_os_package_name


class InfoCollector(BaseFactCollector):
    def collect(self, module=None, collected_facts=None):
        facts = collected_facts or {}
        if not module:
            return {}
        tags = module.params['tags']
        facts['npu_info'] = get_npu_info()
        facts['os_and_arch'] = get_os_and_arch()
        facts['ansible_architecture'] = platform.machine()
        facts['ansible_hostname'] = platform.node()
        facts['local_path'] = '/usr/local'
        facts['ascend_install_path'] = "/usr/local/Ascend"
        facts['ansible_env'] = {
            'HOME': os.path.expanduser('~'),
            'PATH': os.environ.get('PATH')
        }
        os_name, _ = parse_os_release()
        facts['os_name'] = os_name
        if 'dl' in set(tags):
            facts['os_package_name'] = get_os_package_name()
        facts['use_rpm_command'] = not module.get_bin_path('dpkg')
        return facts


def main():
    module = AnsibleModule(argument_spec=dict(
        tags=dict(type='list', required=True),
        is_ipv6=dict(type="bool", required=False, default=False),
    ))
    collector = InfoCollector()
    facts = collector.collect(module)
    module.exit_json(ansible_facts=facts)


if __name__ == '__main__':
    main()
