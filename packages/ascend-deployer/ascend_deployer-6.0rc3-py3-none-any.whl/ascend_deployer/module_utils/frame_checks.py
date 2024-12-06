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

from ansible.module_utils.check_output_manager import check_event
from ansible.module_utils.check_utils import CheckUtil as util


class FrameCheck:

    def __init__(self, module, npu_info, error_messages):
        self.tags = module.params.get("tags")
        self.python_version = module.params.get("python_version")
        self.packages = module.params.get("packages")
        self.error_messages = error_messages
        self.npu_info = npu_info
        self.resources_dir = os.path.join(module.params.get("ascend_deployer_work_dir"), "resources")

    @check_event
    def check_torch(self):
        scene = self.npu_info.get("scene", "")

        if scene == "a910b":
            self.check_kernels("910b")
        if scene == "a910_93":
            self.check_kernels("910_93")

        skip_tags = {"toolkit", "nnae", "pytorch_dev", "pytorch_run", "auto"}
        nnae_pkg = self.packages.get("nnae")
        toolkit_pkg = self.packages.get("toolkit")
        if skip_tags.intersection(set(self.tags)) and (nnae_pkg or toolkit_pkg):
            return

        toolkit_path = "/usr/local/Ascend/ascend-toolkit/set_env.sh"
        nnae_path = "/usr/local/Ascend/nnae/set_env.sh"
        if not os.path.exists(toolkit_path) and not os.path.exists(nnae_path):
            util.record_error("[ASCEND][ERROR] Please install toolkit or nnae before install pytorch.",
                              self.error_messages)

    def check_kernels(self, scene):
        # 1. Check whether kernels have been installed.
        toolkit_kernels_path = "/usr/local/Ascend/ascend-toolkit/latest/opp/built-in/op_impl/ai_core/tbe/kernel/ascend{}/".format(scene)
        nnae_kernels_path = "/usr/local/Ascend/nnae/latest/opp/built-in/op_impl/ai_core/tbe/kernel/ascend{}/".format(scene)
        if os.path.exists(toolkit_kernels_path) or os.path.exists(nnae_kernels_path):
            return
        # 2. Check whether the installed tags contain kernels, pytorch_dev, or pytorch_run.
        skip_tags = {"pytorch_dev", "pytorch_run", "kernels"}
        if skip_tags & set(self.tags):
            return
        # 3. Check whether the kernels package exists during installation in the auto scenario.
        kernels_pkg = self.packages.get("kernels")
        if "auto" in self.tags and kernels_pkg:
            return
        # 4. In other cases.
        util.record_error(
            "[ASCEND][ERROR] For Atlas A2 training series products, please install kernels before install pytorch.",
            self.error_messages)

    @check_event
    def check_tensorflow(self):
        if "3.10" in self.python_version:
            util.record_error("[ASCEND][ERROR] Tensorflow does not support python3.10.* and above. "
                              "please use a earlier python version.", self.error_messages)

    @check_event
    def check_mindspore(self):
        if "3.11" in self.python_version:
            util.record_error("[ASCEND][ERROR] Mindspore does not support python3.11.* and above. "
                              "please use a earlier python version.", self.error_messages)
