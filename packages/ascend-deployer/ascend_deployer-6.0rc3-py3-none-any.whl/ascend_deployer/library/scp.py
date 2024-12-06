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
import glob
import os
import shlex
import subprocess as sp

from ansible.module_utils.basic import AnsibleModule


class Scp:
    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                ip=dict(type="str", required=True),
                remote_user=dict(type="str", required=True),
                passwd=dict(type=str, required=True, no_log=True),
                src=dict(type="str", required=True),
                dest=dict(type="str", required=True),
                fetch=dict(type="bool", required=False, default=False),
            )
        )
        self.ip = self.module.params["ip"]
        self.remote_user = self.module.params["remote_user"]
        self.passwd = self.module.params["passwd"]
        self.src = self.module.params["src"]
        self.dest = self.module.params["dest"]
        self.fetch = self.module.params["fetch"]
        self.scp_src = self._parse_src()
        self.scp_dest = self._parse_dest()
        if self.fetch and not os.path.exists(self.scp_dest):
            os.makedirs(self.scp_dest, mode=0o750)

    def run_scp(self):
        os.environ["SSHPASS"] = self.passwd
        cmd_list = []
        for src in self.scp_src:
            scp_base_cmd = (
                "-o GSSAPIAuthentication=no -o ControlMaster=auto -o ControlPersist=3600s -o StrictHostKeyChecking=no "
                "-o User={} -o ConnectTimeout=10 {} {}".format(self.remote_user, src, self.scp_dest)
            )
            scp_cmd = "scp -r {}".format(scp_base_cmd)
            if os.environ["SSHPASS"]:
                scp_cmd = "sshpass -e scp -r -o {} {}".format("PreferredAuthentications=password", scp_base_cmd)
            cmd_list.append(scp_cmd)
        for cmd in cmd_list:
            self._run_cmd(cmd)
        self.module.exit_json(rc=0, changed=True)

    def _run_cmd(self, scp_cmd):
        result = sp.Popen(
            shlex.split(scp_cmd),
            shell=False,
            universal_newlines=True,
            stderr=sp.PIPE,
            stdout=sp.PIPE,
        )
        _, err = result.communicate()
        if result.returncode != 0:
            self.module.fail_json(msg=err, rc=1, changed=True)

    def _parse_src(self):
        src_list = []
        if not self.fetch:
            for item in self.src.split():
                src_file = " ".join(glob.glob(os.path.realpath(os.path.expanduser(item))))
                if src_file:
                    src_list.append(src_file)
            if not src_list:
                self.module.exit_json(changed=False, rc=0)
            return [" ".join(src_list)]
        for item in self.src.split():
            src_list.append("[{}]:{}".format(self.ip, os.path.expanduser(item)))
        return src_list

    def _parse_dest(self):
        if not self.fetch:
            if self.dest.startswith("~/") or self.dest == "~":
                self.dest = os.path.expanduser(self.dest.replace("~", "~{}".format(self.remote_user)))
            return "[{}]:{}".format(self.ip, self.dest)
        return os.path.realpath(os.path.expanduser(self.dest))


def main():
    scp = Scp()
    scp.run_scp()


if __name__ == "__main__":
    main()
