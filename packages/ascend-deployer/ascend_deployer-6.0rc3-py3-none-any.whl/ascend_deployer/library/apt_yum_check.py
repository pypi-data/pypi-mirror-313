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
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.check_output_manager import check_event
from ansible.module_utils.check_utils import CheckUtil as util
from ansible.module_utils.check_utils import CallCmdException
from ansible.module_utils.common_info import get_os_and_arch


class AptYumCheck(object):
    SKIP_PROBLEMS_DICT = {
        "Kylin_V10Tercel_aarch64": ["kernel-headers", "linux-firmware"],
        "Kylin_V10Tercel_x86_64": ["linux-firmware"],
        "Kylin_V10Sword_aarch64": ["kernel-headers"],
        "CentOS_7.6_aarch64": ["gcc", "openssl11"],
        "CentOS_7.6_x86_64": ["gcc", "openssl11"],
        "OpenEuler_20.03LTS_aarch64": ["linux-firmware"],
        "OpenEuler_20.03LTS_x86_64": ["linux-firmware"],
        "EulerOS_2.8_aarch64": ["device-mapper"]
    }

    def __init__(self):
        self.module = AnsibleModule(argument_spec={})
        self.os_and_arch = get_os_and_arch()
        self.error_messages = []

    def run(self):
        self.apt_yum_check()
        if self.error_messages:
            return self.module.fail_json('\n'.join(self.error_messages))
        self.module.exit_json(changed=True, rc=0)

    @check_event
    def apt_yum_check(self):
        from distutils.spawn import find_executable
        if find_executable("apt-get"):
            cmd_list = ["apt-get check"]
        elif find_executable('yum'):
            cmd_list = ['yum check obsoleted', 'yum check dependencies']
        else:
            raise Exception(
                'The apt-get or yum command cannot be found, please make sure the system is in the support list')
        try:
            for cmd in cmd_list:
                util.run_cmd(cmd)
        except CallCmdException as err:
            error_msg = str(err)
            if self.only_existed_skip_problems(error_msg):
                return
            util.record_error("[ASCEND][[ERROR]] {}".format(error_msg), self.error_messages)

    # When some OS is newly installed, the yum check is abnormal.
    def only_existed_skip_problems(self, error_msg):
        problem_pkgs = self.SKIP_PROBLEMS_DICT.get(self.os_and_arch)
        if not problem_pkgs:
            return False
        expected_err_num = sum(pkg in error_msg for pkg in problem_pkgs)
        actual_err_num = error_msg.count("is obsoleted by")
        if actual_err_num <= expected_err_num:
            return True
        return False


if __name__ == '__main__':
    AptYumCheck().run()
