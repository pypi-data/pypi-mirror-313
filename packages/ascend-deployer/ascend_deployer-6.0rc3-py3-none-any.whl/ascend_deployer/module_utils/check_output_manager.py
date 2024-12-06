# !/usr/bin/env python3
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
import functools
import json
import os
import sys

HOME_PATH = os.path.expanduser('~')
DEPLOY_INFO_OUTPUT_DIR = os.path.join(HOME_PATH, ".ascend_deployer", "deploy_info")
try:
    # 适配python2 json打印中文异常问题
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass


class CheckConfig:

    def __init__(self, check_item, desc_en="", desc_zh="", tip_zh="", tip_en=""):
        self.check_item = check_item
        self.desc_en = desc_en
        self.desc_zh = desc_zh
        self.tip_en = tip_en
        self.tip_zh = tip_zh


CONFIGS = [
    CheckConfig("check_card", desc_en="Check NPU card compatibility", desc_zh="检查NPU卡兼容性"),
    CheckConfig("check_model", desc_en="Check model compatibility", desc_zh="检查模型兼容性"),
    CheckConfig("check_os", desc_en="Check OS compatibility", desc_zh="检查操作系统兼容性",
                tip_en="If the check fails, the operating system is not in the adaptation range. The ascend-deployer"
                       " may also support deployment. Please judge according to the actual situation.",
                tip_zh="若检查失败，操作系统未在已适配范围内，ascend-deployer可能也支持部署。请结合实际情况判断。"),
    CheckConfig("check_sys_pkg", desc_en="Check system packages basic dependency", desc_zh="检查操作系统基本依赖",
                tip_en="If the check fails, the system package may be modified. The ascend-deployer"
                       " may also support deployment. Please judge according to the actual situation.",
                tip_zh="若检查失败，系统依赖包可能已被修改，ascend-deployer可能也支持部署。请结合实际情况判断。"),
    CheckConfig("check_user_privilege_escalation", desc_en="Check whether user privileges to execute "
                                                           "the installation command", desc_zh="检查用户是否提权执行安装命令",
                tip_en="If the check fails, the possible cause is that the installation command is executed by "
                       "a common user, or the su is used to switch the root user or the sudo is used",
                tip_zh="若检查失败，失败原因可能是由普通用户执行安装命令，也可能是使用su切换成root用户或者通过sudo提权执行安装命令。"),
    CheckConfig("check_user", desc_en="Check if user is root", desc_zh="检查用户是否是root"),
    CheckConfig("check_npu_health", desc_en="Check NPU health status", desc_zh="检查NPU健康状态"),
    CheckConfig("check_firmware", desc_en="Check firmware", desc_zh="检查固件"),
    CheckConfig("check_driver", desc_en="Check driver", desc_zh="检查驱动"),
    CheckConfig("check_kernels", desc_en="Check kernels dependency and compatibility", desc_zh="检查kernels依赖和兼容性"),
    CheckConfig("check_tfplugin", desc_en="Check tfplugin compatibility", desc_zh="检查tfplugin兼容性"),
    CheckConfig("check_cann_basic", desc_en="Basic check for cann", desc_zh="安装cann组件的基本检查"),
    CheckConfig("check_torch", desc_en="Check Pytorch dependency", desc_zh="检查Pytorch依赖"),
    CheckConfig("check_tensorflow", desc_en="Check Tensorflow compatibility", desc_zh="检查Tensorflow兼容性"),
    CheckConfig("check_mindspore", desc_en="Check Mindspore compatibility", desc_zh="检查Mindspore兼容性"),
    CheckConfig("check_dl_basic", desc_en="Check DL configuration and root dir space usage rate",
                desc_zh="检查DL配置以及根目录空间占用率"),
    CheckConfig("check_dns", desc_en="Check Whether The DNS Is Configured before install DL",
                desc_zh="检查安装DL组件是否配置了DNS"),
    CheckConfig("check_hccn", desc_en="Check hccn configuration", desc_zh="检查hccn配置"),
]


class CheckStatus(object):
    WAIT = "wait"
    CHECKING = "checking"
    SUCCESS = "success"
    FAILED = "failed"


class CheckOutput(object):

    def __init__(self, check_config, error_msg="", check_status=CheckStatus.WAIT):
        self.check_config = check_config
        self.error_msg = error_msg
        self.check_status = check_status

    def to_json(self):
        res = {
            "check_status": self.check_status,
            "error_msg": self.error_msg
        }
        res.update(vars(self.check_config))
        if self.check_status != CheckStatus.FAILED:
            res.update({
                "tip_en": "",
                "tip_zh": ""
            })
        return res


class CheckOutputManager(object):
    _CHECK_RES_OUTPUT_PATH = os.path.join(DEPLOY_INFO_OUTPUT_DIR, "check_res_output.json")
    _OUTPUT_INTERVAL = 3

    def __init__(self, check_configs):
        self.check_configs = check_configs
        self.check_output_map = {check_config.check_item: CheckOutput(check_config) for check_config in check_configs}
        self.cur_check_item = ""

    @classmethod
    def generate_check_output_manager(cls):
        return CheckOutputManager(CONFIGS)

    def get_check_output(self, check_item):
        return self.check_output_map.setdefault(check_item, CheckOutput(CheckConfig(check_item)))

    def set_error_msg(self, error_msg):
        if not self.cur_check_item:
            return
        self.get_check_output(self.cur_check_item).error_msg = error_msg

    def start_check(self, check_item):
        self.cur_check_item = check_item
        self.get_check_output(check_item).check_status = CheckStatus.CHECKING

    def check_failed(self, check_item):
        check_output = self.get_check_output(check_item)
        check_output.check_status = CheckStatus.FAILED

    def check_success(self, check_item):
        check_output = self.get_check_output(check_item)
        check_output.check_status = CheckStatus.SUCCESS

    def generate_check_output(self):
        return [self.get_check_output(check_config.check_item).to_json() for check_config in self.check_configs]

    def output_check_info_json(self):
        if not os.path.exists(DEPLOY_INFO_OUTPUT_DIR):
            os.makedirs(DEPLOY_INFO_OUTPUT_DIR)
        with open(self._CHECK_RES_OUTPUT_PATH, "w") as output_fs:
            json.dump(self.generate_check_output(), output_fs, indent=4, ensure_ascii=False)


CHECK_OUTPUT_MANAGER = CheckOutputManager.generate_check_output_manager()
CHECK_OUTPUT_MANAGER.output_check_info_json()


def check_event(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        CHECK_OUTPUT_MANAGER.start_check(func.__name__)
        try:
            func(*args, **kwargs)
            if CHECK_OUTPUT_MANAGER.get_check_output(func.__name__).error_msg:
                CHECK_OUTPUT_MANAGER.check_failed(func.__name__)
            else:
                CHECK_OUTPUT_MANAGER.check_success(func.__name__)
        except BaseException as e:
            CHECK_OUTPUT_MANAGER.check_failed(func.__name__)
            raise e
        finally:
            CHECK_OUTPUT_MANAGER.output_check_info_json()

    return wrapper


def set_error_msg(error_msg):
    CHECK_OUTPUT_MANAGER.set_error_msg(error_msg)
