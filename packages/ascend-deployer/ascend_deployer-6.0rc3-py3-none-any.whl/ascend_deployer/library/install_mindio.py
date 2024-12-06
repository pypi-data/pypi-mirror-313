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
import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import common_info, common_utils


class MindIoInstaller:
    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                resources_dir=dict(type="str", required=True),
            )
        )
        self.resources_dir = os.path.expanduser(self.module.params["resources_dir"])
        self.messages = []

    def install_pkg(self):
        arch = common_info.ARCH
        if arch == "x86_64":
            arch = "x86?64"    # old package mix x86-64 and x86_64
        run_files, messages = common_utils.find_files(os.path.join(self.resources_dir, 'run_from_mindio_zip'),
                                                      "Ascend-mindxdl-mindio*{}.run".format(arch))
        self.messages.extend(messages)
        if not run_files:
            self.messages.append("mindio file not found, exiting...")
            return self.module.fail_json(msg="\n".join(self.messages), rc=1, changed=False)
        run_file = run_files[0]
        try:
            _, messages = common_utils.run_command(self.module, "bash {}".format(run_file),
                                                   working_dir=os.path.dirname(run_file))
            self.messages.extend(messages)
            return self.module.exit_json(msg="\n".join(self.messages), rc=0, changed=True)
        except Exception as e:
            self.messages.append(str(e))
            return self.module.fail_json(msg="\n".join(self.messages), rc=1, changed=True)


def main():
    installer = MindIoInstaller()
    installer.install_pkg()


if __name__ == "__main__":
    main()
