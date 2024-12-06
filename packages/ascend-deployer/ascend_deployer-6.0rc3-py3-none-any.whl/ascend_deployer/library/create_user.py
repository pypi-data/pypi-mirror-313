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
import shlex
import subprocess

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(argument_spec=dict(group=dict(type="str", required=True),
                                              user=dict(type="str", required=True)))
    group = module.params["group"]
    user = module.params["user"]
    _, out, _ = module.run_command("getent group {} | wc -l".format(group), use_unsafe_shell=True)
    if not str(out).strip().isdigit():
        return module.fail_json(msg="run cmd: gentent group {} | wc -l failed".format(group))
    if int(out) == 0:
        module.run_command("groupadd {}".format(group), check_rc=True)

    _, out, _ = module.run_command("getent passwd {} | wc -l".format(user), use_unsafe_shell=True)
    if not str(out).strip().isdigit():
        return module.fail_json(msg="run cmd: gentent passwd {} | wc -l failed".format(user))
    if int(out) == 0:
        module.run_command("useradd -g {} -d /home/{} -m {} -s /bin/bash".format(group, user, user), check_rc=True)
    return module.exit_json(rc=0, changed=True)


if __name__ == '__main__':
    main()
