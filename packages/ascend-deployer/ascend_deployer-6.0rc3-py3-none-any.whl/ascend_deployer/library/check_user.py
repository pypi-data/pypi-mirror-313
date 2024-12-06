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
from ansible.module_utils.check_output_manager import check_event, set_error_msg
from ansible.module_utils.check_utils import CheckUtil as util

MAX_CIRCLES = 8


class UserCheck(object):

    def __init__(self):
        self.module = AnsibleModule(argument_spec={})
        self.error_messages = []

    def run(self):
        self.check_user_privilege_escalation()

        if self.error_messages:
            return self.module.fail_json('\n'.join(self.error_messages))
        self.module.exit_json(changed=True, rc=0)

    @check_event
    def check_user_privilege_escalation(self):
        ppid = os.getppid()
        count = 0
        while ppid != 1 and count < MAX_CIRCLES:
            cmd = "ps -ef | grep {}".format(ppid)
            out = util.run_cmd(cmd, util.GREP_RETURN_CODE)
            lines = [line.decode("utf-8") for line in out.splitlines()]
            if not lines or len(lines[0].split()) < 3:
                return
            ppid = lines[0].split()[2]
            count += 1
            for line in lines:
                info = line.strip().split()
                if not info or len(info) < 8:
                    continue
                temp_cmd = info[7]
                if "su" == temp_cmd or temp_cmd.startswith("sudo"):
                    util.record_error("[ASCEND][ERROR] The installation command cannot be executed "
                                      "by a user that is switched from running the 'su - root' "
                                      "or by using 'sudo' to escalate privileges.", self.error_messages)
                    return


if __name__ == '__main__':
    UserCheck().run()
