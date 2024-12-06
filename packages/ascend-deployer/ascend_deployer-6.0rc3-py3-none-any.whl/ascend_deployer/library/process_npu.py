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
import subprocess
import shlex
import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import common_info
from ansible.module_utils.common_info import DeployStatus

DRIVER = "driver"
FIRMWARE = "firmware"
NO_NEED_TO_INSTALL_PLACEHOLDER = "NO_NEED_TO_INSTALL"


class NpuInstallation:
    def __init__(self, module):
        self.force_upgrade_npu = module.params.get("force_upgrade_npu", False)
        self.resource_dir = os.path.expanduser(module.params["resource_dir"])
        self.cus_npu_info = module.params.get("cus_npu_info", "")
        ansible_run_tags = module.params.get("ansible_run_tags", [])
        self.install_target = set()
        if ({"npu", "auto", "dl", "mindspore", "offline_dev", "offline_run",
             "pytorch_dev", "pytorch_run", "tensorflow_dev", "tensorflow_run"} & set(ansible_run_tags)):
            self.install_target.add(FIRMWARE)
            self.install_target.add(DRIVER)
        for target in (DRIVER, FIRMWARE):
            if target in ansible_run_tags:
                self.install_target.add(target)
        self.driver_file_path, self.firmware_file_path = None, None
        self.auto_mode_flag = "auto" in ansible_run_tags
        if DRIVER not in self.install_target or self.auto_mode_flag:
            self.driver_file_path = NO_NEED_TO_INSTALL_PLACEHOLDER
        if FIRMWARE not in self.install_target or self.auto_mode_flag:
            self.firmware_file_path = NO_NEED_TO_INSTALL_PLACEHOLDER
        self.module = module
        self.need_reboot = False
        self.driver_existed_before = False
        self.firmware_existed_before = False
        self.npu_info = common_info.get_npu_info()
        self.messages = []
        self.stdout = []

    def _success_exit(self, result=None):
        return self.module.exit_json(changed=True, rc=0, msg="\n".join(self.messages),
                                     stdout="\n".join(self.stdout), result=result or {})

    def run(self):
        try:
            self._process_npu()
            if self.need_reboot:
                self.stdout.append("[ASCEND][WARNING] you need to reboot for the firmware/driver to take effect")
            return self._success_exit()
        except Exception as e:
            self.messages.append(str(e))
            return self.module.fail_json(msg="\n".join(self.messages))

    def _find_files(self, path, pattern):
        self.messages.append("try to find {} for {}".format(path, pattern))
        matched_files = glob.glob(os.path.join(path, pattern))
        self.messages.append("find files: " + ",".join(matched_files))
        if len(matched_files) > 0:
            return matched_files[0]
        return ""

    def _run_command(self, command, ok_returns=None):
        self.messages.append("calling " + command)
        return_code, out, err = self.module.run_command(shlex.split(command))
        output = out + err
        if not ok_returns:
            ok_returns = [0]
        if return_code not in ok_returns:
            raise Exception("calling {} failed on {}: {}".format(command, return_code, output))
        self.messages.append("output of " + command + " is: " + str(output))
        return output

    def _check_driver_and_npu(self):
        self.driver_existed_before = os.path.exists("/usr/local/Ascend/driver/version.info")
        if not self.driver_existed_before:
            self.messages.append("No driver installed yet, will try to install")
            return
        if self.driver_existed_before and not os.path.isfile("/usr/local/Ascend/driver/tools/upgrade-tool"):
            raise Exception("[ASCEND][WARNING] Driver not installed completely, please reinstall driver first")

        self.firmware_existed_before = os.path.isfile("/usr/local/Ascend/firmware/version.info")

    def _process_npu(self):
        if os.getuid() != 0 and not self.auto_mode_flag:
            raise Exception("[ASCEND] None-root user cannot install firmware/driver!")

        if os.getuid() != 0:  # bypass if not root
            self.messages.append("[ASCEND] Bypass firmware/driver installation as non-root user")
            return self._success_exit({DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP})

        if not self.npu_info.get("scene") or (self.npu_info.get("scene") == 'unknown'):
            if self.auto_mode_flag:
                self.messages.append("[ASCEND][WARNING] Can not detect npu, bypass firmware/driver installation")
                return self._success_exit({DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP})
            raise Exception("[ASCEND][WARNING] Can not detect npu, exit!")

        self._check_driver_and_npu()

        self._find_npu_files()

        # driver already existed, must process firmware first
        if self.driver_existed_before and FIRMWARE in self.install_target:
            self._do_install_npu(FIRMWARE)

        if DRIVER in self.install_target:
            self._do_install_npu(DRIVER)

        # if driver is newly installed, firmware must be installed later
        if not self.driver_existed_before and FIRMWARE in self.install_target:
            self._do_install_npu(FIRMWARE)

    def _find_npu_files(self):
        arch = common_info.ARCH
        if arch == "x86_64":
            arch = "x86?64"  # old package mix x86-64 and x86_64
        uniform_npu_scene = npu_scene = self.npu_info.get("scene")

        # a910b a310b only has uniform package, equal to scene name
        if npu_scene in ("a300i", "a300iduo"):
            uniform_npu_scene = "normalize310p"
        if npu_scene == "train":
            uniform_npu_scene = "normalize910"

        # uniform package has higher priority
        uni_package_path = common_info.get_scene_dict(os.path.expanduser(self.resource_dir)).get(uniform_npu_scene)
        if uni_package_path:
            # uniform packages, like
            # Ascend-hdk-310p-npu-driver_23.0.rc3_linux-aarch64.run
            # Ascend-hdk-310p-npu-firmware_7.0.0.5.242.run
            driver_file_path = self._find_files(uni_package_path, r"*npu-driver*linux*%s*.run" % arch)
            firmware_file_path = self._find_files(uni_package_path, r"*npu-firmware*.run")
            self.driver_file_path = driver_file_path or self.driver_file_path
            self.firmware_file_path = firmware_file_path or self.firmware_file_path
            if self.driver_file_path and self.firmware_file_path:
                return

        # old packages...
        tmp_npu_scene = self._update_scene_by_cus_npu_info()
        package_path = common_info.get_scene_dict(os.path.expanduser(self.resource_dir)).get(tmp_npu_scene)
        if not package_path:
            return
        os_name, os_version = common_info.parse_os_release()

        # first like A300-3010-npu-driver_20.2.2_centos7.6-x86_64.run
        # A300-3010-npu-firmware_6.0.0.run
        driver_file_path = self._find_files(package_path, r"*driver*%s%s*%s.run" % (
            os_name.lower(), os_version, arch))
        firmware_file_path = self._find_files(package_path, r"%s*firmware*.run" %
                                              self.npu_info.get("product", "INVALID"))
        self.driver_file_path = driver_file_path or self.driver_file_path
        self.firmware_file_path = firmware_file_path or self.firmware_file_path
        if self.driver_file_path and self.firmware_file_path:
            return

        # then like A300-3010-npu-driver_20.2.2_linux-x86_64.run
        # A300-3000-3010-npu-firmware_1.76.22.10.220.run
        driver_file_path = self._find_files(package_path, r"*npu-driver*%s.run" % arch)
        firmware_file_path = self._find_files(package_path, r"*npu-firmware*.run")
        self.driver_file_path = driver_file_path or self.driver_file_path
        self.firmware_file_path = firmware_file_path or self.firmware_file_path

    def _update_scene_by_cus_npu_info(self):
        tmp_npu_scene = self.npu_info.get("scene")
        product = self.npu_info.get("product")

        if self.npu_info.get("model") == "Atlas 200I SoC A1":
            return "soc"
        if not self.cus_npu_info:
            return tmp_npu_scene

        if product == "A300i":
            scenes = {"300i-pro": "a300i", "300v-pro": "a300v_pro", "300v": "a300v"}
            tmp_npu_scene = scenes.get(self.cus_npu_info)
            if not tmp_npu_scene:
                raise Exception("[ASCEND][FAILURE] When NPU is 300i/300v, cus_npu_info must be set to 300i-pro "
                                "or 300v-pro or 300v")
        elif product == "A300t":
            scenes = {"300t": "train", "300t-pro": "trainpro"}
            tmp_npu_scene = scenes.get(self.cus_npu_info)
            if not tmp_npu_scene:
                raise Exception("[ASCEND][FAILURE] When NPU is 300t/300t-pro, cus_npu_info must be set to "
                                "300t or 300t-pro")
        elif self.cus_npu_info:
            raise Exception("[ASCEND][FAILURE] When NPU is not 300i/300v or 300t-9000/300t-pro, "
                            "cus_npu_info must be undefined")

        return tmp_npu_scene

    def _do_install_npu(self, package_type):
        run_file = self.driver_file_path
        extra_param = ""
        if self.driver_existed_before:
            action = "upgrade"
        else:
            action = "full"
            extra_param = "--install-for-all"

        if package_type == FIRMWARE:
            run_file = self.firmware_file_path
            extra_param = ""
            if self.firmware_existed_before:
                action = "upgrade"
            else:
                action = "full"

        if run_file == NO_NEED_TO_INSTALL_PLACEHOLDER:
            self.messages.append("[ASCEND] Driver/firmware file not found or no need to install, BYPASS")
            return self._success_exit({DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP})

        if not run_file:
            raise Exception("[ASCEND][FAILURE] Driver/firmware file not found!")
        command = "bash %s --nox11 --%s --quiet %s " % (run_file, action, extra_param)
        self._run_command(command, ok_returns=[0, 2])
        self.messages.append("[ASCEND] %s is installed successfully" % package_type)
        package_name = "Driver" if package_type == DRIVER else "Firmware"
        self.stdout.append("[ASCEND] {} install processing is 100%".format(package_name))
        self.need_reboot = True
        return


def main():
    module = AnsibleModule(
        argument_spec=dict(
            force_upgrade_npu=dict(type="bool", required=False),
            resource_dir=dict(type="str", required=True),
            cus_npu_info=dict(type="str", required=True),
            ansible_run_tags=dict(type="list", required=True),
        )
    )
    NpuInstallation(module).run()


if __name__ == "__main__":
    main()
