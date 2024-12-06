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
import glob
import os

from ansible.module_utils.check_output_manager import check_event
from ansible.module_utils.check_utils import CheckUtil as util


class CANNCheck:
    def __init__(self, module, npu_info, error_messages):
        self.module = module
        self.tags = module.params.get("tags")
        self.resource_dir = os.path.join(module.params.get("ascend_deployer_work_dir"), "resources")
        self.python_version = module.params.get("python_version")
        self.packages = module.params.get("packages")
        self.npu_info = npu_info
        self.error_messages = error_messages

    @check_event
    def check_kernels(self):
        if self.npu_info.get("scene") == "infer":
            util.record_error("[ASCEND][ERROR] kernels not support infer scene", self.error_messages)
            return

        kernels_pkg = self.packages.get("kernels")
        if not kernels_pkg:
            util.record_error("[ASCEND][ERROR] Do not find kernels package, please download kernels package first.",
                              self.error_messages)
            return

        skip_tags = {"toolkit", "nnae", "nnrt", "auto", "dl", "pytorch_dev", "pytorch_run",
                     "tensorflow_dev", "tensorflow_run", "mindspore_scene", "offline_dev"}
        nnae_pkg = self.packages.get("nnae")
        toolkit_pkg = self.packages.get("toolkit")
        nnrt_pkg = self.packages.get("nnrt")
        if skip_tags.intersection(set(self.tags)) and (nnae_pkg or toolkit_pkg or nnrt_pkg):
            return

        script_info = os.path.basename(kernels_pkg).split("_")
        if len(script_info) < 2:
            util.record_error("[ASCEND][ERROR] Do not find kernels package, please download kernels package first.",
                              self.error_messages)
            return
        script_name_split = os.path.basename(kernels_pkg).split("_")
        index = 1
        kernels_version = script_name_split[index] if len(script_name_split) > index else None
        if not kernels_version:
            return self.module.fail_json(
                changed=False,
                rc=1,
                msg=(
                    "[ASCEND]cann not find version from name {}, please check.".format(os.path.basename(kernels_pkg))
                ),
            )
        if (not glob.glob("/usr/local/Ascend/*/{}/*/ascend_toolkit_install.info".format(kernels_version))
                and not glob.glob("/usr/local/Ascend/*/{}/ascend_nnae_install.info".format(kernels_version))
                and not glob.glob("/usr/local/Ascend/*/{}/*/ascend_nnrt_install.info".format(kernels_version))):
            util.record_error("[ASCEND][ERROR] Please install toolkit or nnae or nnrt before install kernels",
                              self.error_messages)

    def check_driver_installation(self):
        ascend_info_path = "/etc/ascend_install.info"
        if not os.path.isfile(ascend_info_path):
            return
        with open(ascend_info_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "Driver_Install_Path_Param" not in line:
                    continue
                driver_install_path = line.split("=")[-1].strip()
                if not os.path.isfile(os.path.join(driver_install_path, "driver/version.info")):
                    util.record_error("[ASCEND][ERROR] The /etc/ascend_install.info file exists in the environment, "
                                      "and the file records the driver installation path. However, "
                                      "the driver/version.info does not exist in the installation path. "
                                      "Please check the driver is correctly installed.", self.error_messages)
                    return

    def check_cann_install_path_permission(self):
        install_path = "/usr/local/Ascend"
        if not os.path.isdir(install_path):
            return
        if os.stat(install_path).st_uid != 0:
            util.record_error("[ASCEND][ERROR] The owner of the cann installation dir "
                              "'/usr/local/Ascend' must be root, change the owner to root", self.error_messages)
            return

        mode = os.stat(install_path).st_mode
        permissions = oct(mode)[-3:]
        if int(permissions) != 755:
            util.record_error("[ASCEND][ERROR] When installing cann, the user and group of the installation path "
                              "must be root, and the permission must be 755. ", self.error_messages)
        return

    @check_event
    def check_cann_basic(self):
        self.check_driver_installation()
        self.check_cann_install_path_permission()

    @check_event
    def check_tfplugin(self):
        if "3.10." in self.python_version:
            util.record_error("[ASCEND][ERROR] Tfplugin dose not support python3.10.* and above. "
                              "please use a earlier python version.", self.error_messages)
