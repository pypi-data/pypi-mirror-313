#!/usr/bin/env python3
# coding: utf-8
# Copyright 2024 Huawei Technologies Co., Ltd
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

import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_utils import run_command, get_cmd_color_str

IPV4_PATTERN = re.compile(r'inet (\d+\.\d+\.\d+\.\d+)')
IPV6_PATTERN = re.compile(r'inet6 ([a-fA-F0-9:]+)')

class LocalhostCheck(object):

    def __init__(self):
        self.module = AnsibleModule(argument_spec=dict(
            master_groups=dict(type='list')
        ))
        self.master_groups = self.module.params['master_groups']

    def get_local_all_ips(self):
        # Run the ip addr or ifconfig command to obtain network interface information.
        ips_list = []
        try:
            lines, _ = run_command(self.module, 'ip addr')
        except FileNotFoundError:
            lines, _ = run_command(self.module, 'ifconfig')
        for line in lines.splitlines():
            line = line.strip()
            if 'inet' not in line or ' ' not in line:
                continue
            for pattern in [IPV4_PATTERN, IPV6_PATTERN]:
                search = pattern.search(line)
                if search:
                    ips_list.append(search.group(1))
                    break
        return ips_list

    def run(self):
        local_all_ips = self.get_local_all_ips()
        if bool((set(local_all_ips) & set(self.master_groups))) or 'localhost' in self.master_groups:
            message = get_cmd_color_str(
                '[ASCEND][WARNING]: It is recommended to select non-master nodes for running execution task',
                'yellow')
            self.module.warn(message)

        self.module.exit_json(changed=True, rc=0)


if __name__ == '__main__':
    LocalhostCheck().run()
