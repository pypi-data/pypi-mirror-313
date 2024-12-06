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
import re
import subprocess

from ansible.module_utils.check_output_manager import set_error_msg
from ansible.module_utils.common_info import get_npu_info


class CallCmdException(Exception):
    pass


class CheckUtil:
    GREP_RETURN_CODE = [0, 1]

    @classmethod
    def get_card(cls):
        npu_info = get_npu_info()
        scene = npu_info.get("scene")
        if scene == "a300i" or scene == "a300iduo":
            return "310p"
        elif scene == "train":
            return "910"
        elif scene == "a910b":
            return "910b"
        elif scene == "a910_93":
            return "910_93"
        else:
            return "--"

    @classmethod
    def run_cmd(cls, cmd, success_code=None):
        sp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = sp.communicate()
        if success_code:
            if sp.returncode not in success_code:
                raise CallCmdException("call cmd {} failed, reason: {}".format(cmd, out + err))
            return out

        if sp.returncode != 0:
            raise CallCmdException("call cmd {} failed, reason: {}".format(cmd, out + err))
        return out

    @classmethod
    def record_error(cls, msg, error_messages):
        if msg and msg not in error_messages:
            error_messages.append(msg)
            set_error_msg(msg)

    @classmethod
    def find_file(cls, resources, file_name):
        for _, _, files in os.walk(resources):
            for file in files:
                if re.match(file_name, file):
                    return file

        return None
