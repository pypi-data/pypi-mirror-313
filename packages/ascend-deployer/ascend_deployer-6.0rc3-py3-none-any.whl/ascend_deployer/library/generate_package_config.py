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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.facts.collector import BaseFactCollector
from ansible.module_utils.check_utils import CheckUtil


class PackageInfoCollector(BaseFactCollector):
    def collect(self, module=None, collected_facts=None):
        facts = collected_facts or {}
        if not module:
            return {}

        work_dir = module.params['ascend_deployer_work_dir']
        resource_dir = os.path.join(work_dir, "resources")
        frame_dir = os.path.join(resource_dir, "pylibs")
        packages = ["npu", "mindspore", "tensorflow", "torch", "tfplugin", "nnrt", "nnae", "toolbox", "toolkit",
                    "kernels"]
        package_config = dict()
        card = CheckUtil.get_card()
        for package in packages:
            source_dir = resource_dir
            pattern = "Ascend-cann-{}.*(zip|run)".format(package)
            if package in ["mindspore", "tensorflow", "torch"]:
                source_dir = frame_dir
                pattern = "{}.*whl".format(package)
            elif package == "npu":
                if card == "910_93":
                    pattern = "Atlas-A3-hdk-npu.*zip"
                else:
                    pattern = "Ascend-hdk-{}-npu.*zip".format(card)
            elif package == "kernels":
                if card == "910_93":
                    pattern = "Atlas-A3-cann-kernels.*(zip|run)"
                else:
                    pattern = "Ascend-cann-kernels-{}.*(zip|run)".format(card)
            elif package == "toolbox":
                pattern = "Ascend-mindx-toolbox.*zip"

            file = CheckUtil.find_file(source_dir, pattern)
            if file:
                package_config[package] = file
        facts['packages'] = package_config
        return facts


def main():
    module = AnsibleModule(argument_spec=dict(
        ascend_deployer_work_dir=dict(type="str", required=False, default=False),
    ))
    collector = PackageInfoCollector()
    facts = collector.collect(module)
    module.exit_json(ansible_facts=facts)


if __name__ == '__main__':
    main()
