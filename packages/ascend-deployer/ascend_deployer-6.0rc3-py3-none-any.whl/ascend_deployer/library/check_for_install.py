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
from ansible.module_utils.common_info import get_os_and_arch, get_npu_info, need_skip_sys_package
from ansible.module_utils.common_utils import run_command
from ansible.module_utils.compatibility_config import EOL_CARD, EOL_MODEL, CARD_DICT, MODEL_TAGS_NOT_SUPPORT, \
    OS_ARCH_TAGS_SUPPORT
from ansible.module_utils.dl_checks import DLCheck
from ansible.module_utils.frame_checks import FrameCheck
from ansible.module_utils.npu_checks import NPUCheck
from ansible.module_utils.cann_checks import CANNCheck
from ansible.module_utils.check_utils import CheckUtil as util

EOL_MSG = "[ASCEND] The lifecycle of {} is over and is no longer supported"
SUPPORT_MSG = "[ASCEND] {} has no support for {} on this device"

MAX_CIRCLES = 8


class CompatibilityCheck(object):

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                tags=dict(type='list'),
                python_version=dict(type='str', required=False),
                force_upgrade_npu=dict(type="bool", required=False),
                group_names=dict(type="list"),
                hosts_name=dict(type="str", required=False),
                master_groups=dict(type="list", required=False),
                worker_groups=dict(type="list", required=False),
                host_info=dict(type="dict", required=False),
                current_hostname=dict(type="str", required=False),
                ascend_deployer_work_dir=dict(type='str', required=True),
                npu_num=dict(type='int', required=False),
                packages=dict(type='dict', required=True),
                node_name=dict(type="str", required=True),
                cluster_info=dict(type='dict', required=True),
            ))
        self.tags = list(filter(bool, self.module.params.get('tags', [])))
        if 'all' in self.tags:
            self.tags.remove('all')
        self.group_names = self.module.params.get("group_names")
        self.worker_groups = self.module.params.get("worker_groups")
        self.current_hostname = self.module.params.get("current_hostname")
        self.hosts_name = self.module.params.get("hosts_name").split(",")
        self.packages = self.module.params.get("packages")
        self.npu_info = get_npu_info()
        self.os_and_arch = get_os_and_arch()
        self.card = util.get_card()
        self.error_messages = []
        self.dl_check = DLCheck(self.module, self.error_messages)
        self.frame_checks = FrameCheck(self.module, self.npu_info, self.error_messages)
        self.npu_check = NPUCheck(self.module, self.error_messages)
        self.cann_check = CANNCheck(self.module, self.npu_info, self.error_messages)
        self.tags_config = self.init_config()
        self.resources_dir = os.path.join(self.module.params.get("ascend_deployer_work_dir"), "resources")

    def base_check(self):
        self.check_card()
        self.check_model()
        self.check_os()
        self.check_sys_pkg()
        self.check_user()

    def feature_check(self):
        for tag in self.tags:
            tag_config = self.tags_config.get(tag)
            if not tag_config:
                continue
            if not set(self.group_names).intersection(set(tag_config.get("nodes"))):
                return
            checks = self.tags_config.get(tag).get("checks")
            if tag == "auto":
                checks = self.filter_auto_checks()
            if tag == "dl" and self.current_hostname not in self.worker_groups:
                checks.remove(self.npu_check.check_npu)

            for check_handler in checks:
                check_handler()

    def run(self):
        self.base_check()
        self.feature_check()

        if self.error_messages:
            self.error_messages.append("For check details, please see ~/.ascend_deployer/"
                                       "deploy_info/check_res_output.json.")
            return self.module.fail_json('\n'.join(self.error_messages))
        self.module.exit_json(changed=True, rc=0)

    @check_event
    def check_user(self):
        uid = os.getuid()
        if uid != 0:
            util.record_error("[ASCEND][ERROR] ascend-deployer only supports root user, please switch to root user.",
                              self.error_messages)

    @check_event
    def check_card(self):
        card = self.npu_info.get('card')
        if card in EOL_CARD:
            util.record_error(EOL_MSG.format(card), self.error_messages)
        support_os_arch_list = CARD_DICT.get(card)
        if support_os_arch_list and self.os_and_arch not in support_os_arch_list:
            util.record_error("Check card failed: " + SUPPORT_MSG.format(card, self.os_and_arch), self.error_messages)

    @check_event
    def check_model(self):
        model = self.npu_info.get('model')
        if model in EOL_MODEL:
            util.record_error(EOL_MSG.format(model), self.error_messages)
        unsupported_tags = MODEL_TAGS_NOT_SUPPORT.get(model, [])
        for tag in self.tags:
            if tag in unsupported_tags:
                util.record_error("Check model failed: " + SUPPORT_MSG.format(tag, model), self.error_messages)

    @check_event
    def check_os(self):
        not_support_components = []
        supported_tags = OS_ARCH_TAGS_SUPPORT.get(self.os_and_arch, [])
        infer_devices = ('A300i-pro', 'A300i-duo', 'A200i-a2', 'Atlas 800I A2')
        card = self.npu_info.get('card')
        for tag in self.tags:
            if tag not in supported_tags or (card in infer_devices and tag == 'mindspore'):
                # infer devices do not support mindspore anymore.
                not_support_components.append(tag)
        if not_support_components:
            util.record_error("Check os failed: " + SUPPORT_MSG.format(','.join(not_support_components), self.os_and_arch),
                              self.error_messages)

    @check_event
    def check_sys_pkg(self):
        if "sys_pkg" not in self.tags and "auto" not in self.tags:
            return

        if need_skip_sys_package(self.os_and_arch):
            util.record_error("[ASCEND][ERROR] Not support installing sys_pkg on {}".format(self.os_and_arch),
                              self.error_messages)

        need_print_sys_pkg_warning = False
        try:
            if not self.module.get_bin_path("yum"):
                return
            output, messages = run_command(self.module, "yum history")
            self.module.log(" ".join(messages))
            self.module.log(output)
            for line in output.splitlines():
                # e.g.:
                # Loaded plugins: fastestmirror
                # ID     | Command line             | Date and time    | Action(s)      | Altered
                # -------------------------------------------------------------------------------
                #     22 | install -y screen        | 2024-03-01 09:03 | Install        |    1
                words = line.split()
                if len(words) > 1 and words[0].isdigit() and words[0] != '1':
                    need_print_sys_pkg_warning = True
                    break
        except Exception as e:
            self.module.log(str(e))
            need_print_sys_pkg_warning = True
        if need_print_sys_pkg_warning:
            util.record_error("ascend-deployer is designed for initial system installation. After the "
                              "initial installation, there may be changes to the system packages on "
                              "this system. In this case, ascend-deployer may not be able to handle the"
                              " system packages correctly. If you encounter errors in this scenario, "
                              "please consider not using the auto nor sys_pkg parameters by ascend-deployer."
                              " Instead, rely on the instructions in the NPU and CANN documents to "
                              "manually install the system packages.", self.error_messages)

    def filter_cann_check(self):
        plugins = ["tfplugin", "nnrt", "nnae", "toolbox", "toolkit", "kernels"]
        for plugin in plugins:
            if self.packages.get(plugin):
                return True

        return False

    def filter_auto_checks(self):
        """
        auto场景时，过滤不需要的检查项

        """
        res = []
        checks = self.tags_config.get("auto").get("checks")
        for check in checks:
            name = check.__name__
            plugin = name.split("_")[1]
            if plugin == "cann" and self.filter_cann_check():
                res.append(check)
            elif self.packages.get(plugin):
                res.append(check)

        return res

    def init_config(self):
        return {
            'resilience-controller': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns],
                                      "nodes": self.hosts_name},
            'npu': {"checks": [self.npu_check.check_npu], "nodes": self.hosts_name},
            'firmware': {"checks": [self.npu_check.check_npu_health, self.npu_check.check_firmware],
                         "nodes": self.hosts_name},
            'driver': {"checks": [self.npu_check.check_npu_health, self.npu_check.check_driver],
                       "nodes": self.hosts_name},
            'pytorch_dev': {"checks": [self.npu_check.check_npu, self.cann_check.check_kernels,
                                       self.frame_checks.check_torch],
                            "nodes": self.hosts_name},
            'pytorch_run': {"checks": [self.npu_check.check_npu, self.cann_check.check_kernels,
                                       self.frame_checks.check_torch],
                            "nodes": self.hosts_name},
            'tensorflow_dev': {"checks": [self.npu_check.check_npu, self.frame_checks.check_tensorflow,
                                          self.cann_check.check_kernels, self.cann_check.check_tfplugin],
                               "nodes": self.hosts_name},
            'tensorflow_run': {"checks": [self.npu_check.check_npu, self.frame_checks.check_tensorflow,
                                          self.cann_check.check_kernels, self.cann_check.check_tfplugin],
                               "nodes": self.hosts_name},
            'npu-exporter': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns],
                             "nodes": ["master"]},
            'noded': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns],
                      "nodes": ["worker"]},
            'volcano': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns],
                        "nodes": self.hosts_name},
            'ascend-operator': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns], "nodes": ["master"]},
            'clusterd': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns], "nodes": ["master"]},
            'kernels': {"checks": [self.cann_check.check_kernels, self.cann_check.check_cann_basic],
                        "nodes": self.hosts_name},
            'dl': {"checks": [self.npu_check.check_npu, self.dl_check.check_dl_basic, self.dl_check.check_dns],
                   "nodes": self.hosts_name},
            'tfplugin': {"checks": [self.cann_check.check_tfplugin, self.cann_check.check_cann_basic],
                         "nodes": self.hosts_name},
            'toolkit': {"checks": [self.cann_check.check_cann_basic], "nodes": self.hosts_name},
            'nnrt': {"checks": [self.cann_check.check_cann_basic], "nodes": self.hosts_name},
            'nnae': {"checks": [self.cann_check.check_cann_basic], "nodes": self.hosts_name},
            'toolbox': {"checks": [self.cann_check.check_cann_basic], "nodes": self.hosts_name},
            'mindspore': {"checks": [self.frame_checks.check_mindspore], "nodes": self.hosts_name},
            'mindspore_scene': {"checks": [self.npu_check.check_npu, self.frame_checks.check_mindspore,
                                           self.cann_check.check_cann_basic, self.cann_check.check_kernels],
                                "nodes": self.hosts_name},
            'auto': {"checks": [self.npu_check.check_npu, self.frame_checks.check_tensorflow,
                                self.frame_checks.check_mindspore, self.cann_check.check_kernels,
                                self.frame_checks.check_torch, self.cann_check.check_tfplugin,
                                self.cann_check.check_cann_basic],
                     "nodes": self.hosts_name},
            'ascend-device-plugin': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns],
                                     "nodes": ["worker"]},
            'ascend-docker-runtime': {"checks": [self.dl_check.check_dns], "nodes": ["worker"]},
            'mindio': {"checks": [self.dl_check.check_dns, self.dl_check.check_mindio_install_path_permission],
                       "nodes": ["worker"]},
            'offline_dev': {"checks": [self.npu_check.check_npu, self.cann_check.check_kernels],
                            "nodes": self.hosts_name},
            'offline_run': {"checks": [self.npu_check.check_npu], "nodes": self.hosts_name},
            'tensorflow': {"checks": [self.frame_checks.check_tensorflow], "nodes": self.hosts_name},
            'hccl-controller': {"checks": [self.dl_check.check_dl_basic, self.dl_check.check_dns], "nodes": ["master"]},
            'pytorch': {"checks": [self.frame_checks.check_torch], "nodes": self.hosts_name},
        }


if __name__ == '__main__':
    CompatibilityCheck().run()
