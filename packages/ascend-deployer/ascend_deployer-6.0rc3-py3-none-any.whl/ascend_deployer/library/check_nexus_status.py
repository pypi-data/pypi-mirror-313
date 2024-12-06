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
import re
import shlex
import subprocess as sp
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_info import need_skip_sys_package


def check_nexus_start_status(module, timeout=600):
    nexus_status_file = os.path.expanduser("~/.local/nexus.sentinel")
    start = 0
    while start <= timeout:
        if os.path.exists(nexus_status_file):
            return ""
        start += 1
        time.sleep(1)
    return module.fail_json(msg="nexus start failed", rc=1, changed=True)


def check_repo_index(module, os_and_arch, timeout=120):
    start = 0
    while start <= timeout:
        check_log_cmd = "docker logs nexus"
        result = sp.Popen(
            shlex.split(check_log_cmd),
            shell=False,
            universal_newlines=True,
            stderr=sp.PIPE,
            stdout=sp.PIPE,
        )
        out, _ = result.communicate()
        if re.search(r"Finished rebuilding .* {}".format(os_and_arch), out):
            return module.exit_json(rc=0, changed=True)
        start += 1
        time.sleep(1)
    return module.fail_json(
        msg="Please ensure that the system dependencies for {} have been downloaded".format(os_and_arch),
        rc=1,
        changed=True,
    )


def main():
    module = AnsibleModule(argument_spec=dict(os_and_arch=dict(type="str", required=True)))
    os_and_arch = module.params["os_and_arch"]
    if need_skip_sys_package(os_and_arch):
        return module.exit_json(rc=0, changed=True)
    check_nexus_start_status(module)
    if "Ubuntu" not in os_and_arch and "Debian" not in os_and_arch:
        check_repo_index(module, os_and_arch)
    return module.exit_json(rc=0, changed=True)


if __name__ == "__main__":
    main()
