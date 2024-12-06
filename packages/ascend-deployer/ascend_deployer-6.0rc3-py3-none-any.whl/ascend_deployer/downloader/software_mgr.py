#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
"""software manager,管理可选下载的软件"""
import collections
import json
import os
from typing import List, Dict

from .download_util import State

CUR_DIR = os.path.dirname(__file__)
SOFT_DIR = os.path.join(CUR_DIR, 'software')


class BaseModel:

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return str(self)

    @staticmethod
    def _to_type_list(clazz, dict_list: List[Dict]):
        return [clazz(**dic) for dic in (dict_list or [])]


class PkgInfo(BaseModel):

    def __init__(self, filename="", url="", sha256="", dest="", remark="", python="cp37", *args, **kwargs):
        self.filename = filename
        self.url = url
        self.sha256 = sha256
        self.dest = dest
        self.python = python
        self.remark = remark


class FrameworkWhl(BaseModel):

    def __init__(self, system="", whl: List[Dict] = None, *args, **kwargs):
        self.system = system
        self.whl: List[PkgInfo] = self._to_type_list(PkgInfo, whl)


class SysPkg(BaseModel):

    def __init__(self, name="", dst_dir="", url="", sha256="", version="", *args, **kwargs):
        self.name = name
        self.dst_dir = dst_dir
        self.url = url
        self.sha256 = sha256
        self.version = version


class SystemPkg(BaseModel):

    def __init__(self, system: str, sys: List[Dict], *args, **kwargs):
        self.system = system
        self.sys: List[SysPkg] = self._to_type_list(SysPkg, sys)


class SoftwareVersion(BaseModel):

    def __init__(self, name="", version="", *args, **kwargs):
        self.name = name
        self.version = version

    def __str__(self):
        return self.name + "_" + self.version


class PylibInfo(object):

    def __init__(self, name, version="", cp=""):
        self.name = str(name).strip()
        self.version = version.strip()
        self.cp = cp.strip()

    @classmethod
    def parse_line(cls, line: str = ""):
        if "==" not in line:
            return cls(line)
        return cls(*line.split("=="))


class SoftwareInfo(BaseModel):

    def __init__(self, name: str = "", default: bool = False, version: str = "", required_soft: List[Dict] = None,
                 other: List[Dict] = None, framework_whl: List[Dict] = None, systems: List[Dict] = None, *args,
                 **kwargs):
        self.name = name
        self.default = default
        self.version = version
        self.required_soft: List[SoftwareVersion] = self._to_type_list(SoftwareVersion, required_soft)
        self.other: List[PkgInfo] = self._to_type_list(PkgInfo, other)
        self.framework_whl: List[FrameworkWhl] = self._to_type_list(FrameworkWhl, framework_whl)
        self.systems: List[SystemPkg] = self._to_type_list(SystemPkg, systems)
        self.framework_whl_map = {item.system: item.whl for item in self.framework_whl}
        self.system_pkg_map = {item.system: item.sys for item in self.systems}


class SoftwareMatchPair:

    def __init__(self, source: SoftwareVersion, target: SoftwareVersion):
        self.source = source
        self.target = target


class SoftwareMatchResult:

    def __init__(self, unmatch_software_pair: SoftwareMatchPair, support_match_software: SoftwareMatchPair):
        self.unmatch_software = unmatch_software_pair
        self.match_software_pair = support_match_software


class SoftwareMgr:
    DOWNLOADER_PATH = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        self.all_software_config = self._software_init()
        self.sys_software_list = [software for software in self.all_software_config if software.systems]
        self.framework_whl_list = [software for software in self.all_software_config if software.framework_whl]
        self.other_software_list = [software for software in self.all_software_config if software.other]

    @staticmethod
    def _load_software(json_file) -> SoftwareInfo:
        with open(json_file) as fs:
            json_obj = json.load(fs)
        return SoftwareInfo(**json_obj)

    def _software_init(self) -> List[SoftwareInfo]:
        all_software = []
        for _, _, files in os.walk(SOFT_DIR):
            for file_name in files:
                if file_name.endswith('json'):
                    all_software.append(self._load_software(os.path.join(SOFT_DIR, file_name)))
        return all_software

    def get_software_name_version(self, software):
        if '==' in software:
            software_split_list = software.split('==')
            name = software_split_list[0]
            version = software_split_list[1]
        else:
            name = software
            version = next(
                (soft.version for soft in self.all_software_config if soft.name == software and soft.default), "")
        return name, version

    def get_software_other(self, name, version=None) -> List[PkgInfo]:
        """
        获取软件的其他依赖项
        :param in:  name      软件名
        :param in:  version   软件版本
        :return:   安装软件name所需要下载的其他内容列表
        """
        for soft in self.other_software_list:
            if soft.name.lower() == name.lower() and (version is None or soft.version == version):
                return soft.other
        return []

    def get_software_framework(self, name, sys_name, version=None) -> List[PkgInfo]:
        """
        获取软件依赖的操作系统依赖
        :param in:  name      软件名
        :param in:  sys_name  操作系统
        :param in:  version   软件版本
        :return:   软件name在操作系统sys_name下的framework whl
        """
        for soft in self.framework_whl_list:
            if soft.name.lower() == name.lower() and (version is None or soft.version == version):
                return soft.framework_whl_map.get(sys_name, [])
        return []

    def get_software_sys(self, name, sys_name, version=None) -> List[SysPkg]:
        """
        获取软件依赖的操作系统依赖
        :param in:  name      软件名
        :param in:  sys_name  操作系统
        :param in:  version   软件版本
        :return:   软件name在操作系统sys_name下的系统依赖列表
        """
        for soft in self.sys_software_list:
            if soft.name.lower() == name.lower() and (version is None or soft.version == version):
                return soft.system_pkg_map.get(sys_name, [])
        return []

    def get_name_version(self, pkg_item, std_out=True):
        name_version = pkg_item
        if pkg_item and '==' not in pkg_item and '_' not in pkg_item:
            name, version = self.get_software_name_version(pkg_item)
            name_version = name + '_' + version
            if std_out:
                print('version of {} not selected, use {} as default'.format(pkg_item, name_version))
        return name_version.replace('==', '_')

    def check_version_matched(self, os_list, soft_list):
        """
        check version matched between CANN and MindSpore
        :param soft_list:download package list
        :return:err_with_exit msg, err_with_ask msg
        """
        item_counter = collections.defaultdict(int)
        version_dict = collections.defaultdict(lambda: "")
        AI_FRAMEWORK = ("MindSpore", "Torch-npu", "TensorFlow")
        frameworks = set()
        for soft in soft_list:
            name_version = self.get_name_version(soft)
            for item in ("DL", "MindSpore", "MindStudio", "Torch-npu", "CANN", "TensorFlow", "NPU"):
                if item not in soft:
                    continue
                if item in AI_FRAMEWORK:
                    frameworks.add(item)
                item_counter[item] += 1
                version_dict[item] = name_version
                if item_counter.get(item, 0) > 1:
                    return State.EXIT, "Only one {} is allowed, Please reselect and try again".format(item)
        if len(frameworks) > 1:
            return State.EXIT, ("Only one ai framework(MindSpore/Torch/TensorFlow) is allowed due to dependency "
                                "conflict, Please reselect and try again")

        warning_messages = ''
        for name, version in version_dict.items():
            if "CANN" not in version:
                warning_messages += self.check_cann_matching(version_dict.get("CANN", ""), version)
        versions = [v.split("_")[1] for k, v in version_dict.items() if k == "DL"]
        for version in versions:
            with open(os.path.join(self.DOWNLOADER_PATH, f'software/DL_{version}.json'), "r") as f:
                dl_info = json.load(f)
                support_os_list = dl_info.get("support_os_list", [])
            not_support_list = [i for i in os_list if i.replace('==', '_') not in support_os_list]
            if not_support_list:
                if item_counter.get('DL', 0) > 0:
                    return State.EXIT, "ascend-deployer do not support install DL on {}".format(not_support_list)

        if warning_messages:
            return State.ASK, warning_messages

        return State.NONE, ""

    def check_cann_matching(self, cann_version, name_version):
        warning_message = ""
        version_match_json = os.path.join(self.DOWNLOADER_PATH, 'version_match.json')
        with open(version_match_json, 'r', encoding='utf-8') as json_file:
            version_match_data = json.load(json_file)
        matching_cann = version_match_data.get(name_version)
        if "DL" in name_version and cann_version == "":
            return warning_message

        if not cann_version and name_version not in version_match_data.get("NoneMatched", []):
            return "no CANN for {}, ".format(name_version)

        matching_component_list = []
        for component, cann in version_match_data.items():
            if cann == cann_version and component.split("_")[0] == name_version.split("_")[0]:
                matching_component_list.append(component)
        matching_component = '/'.join(matching_component_list) if matching_component_list else ""
        if matching_cann != cann_version and name_version not in version_match_data.get("NoneMatched", []):
            warning_message = "{} need matching {}, ".format(cann_version, matching_component)
            if not matching_component:
                warning_message = "{} has no matching {}, ".format(cann_version, name_version.split("_")[0])
        return warning_message

    @staticmethod
    def _some_matched(left, right):
        return any((left, right)) and not all((left, right))

    @staticmethod
    def _build_warning_messages(soft_match_result: SoftwareMatchResult):
        msg_list = []
        support_match_software = soft_match_result.match_software_pair
        msg_list.append("{}_{} need matching {}_{},"
                        .format(support_match_software.source.name, support_match_software.source.version,
                                support_match_software.target.name, support_match_software.target.version))
        return " ".join(msg_list)

    def check_download_software_matching(self, soft_list):
        support_soft_match_list = []
        soft_version_list = [self.get_software_name_version(soft) for soft in soft_list]
        soft_version_map = {name: version for name, version in soft_version_list}
        for soft_config in self.all_software_config:
            soft_version = soft_version_map.get(soft_config.name)
            if not soft_version or soft_version != soft_config.version:
                continue
            for required_soft in soft_config.required_soft:
                selected_soft_version = soft_version_map.get(required_soft.name)
                if selected_soft_version and required_soft.version != selected_soft_version:
                    source_soft_ver = SoftwareVersion(soft_config.name, soft_config.version)
                    unmatched_soft_pair = SoftwareMatchPair(source_soft_ver,
                                                            SoftwareVersion(required_soft.name, selected_soft_version))
                    match_software_pair = SoftwareMatchPair(source_soft_ver,
                                                            SoftwareVersion(required_soft.name, required_soft.version))
                    support_soft_match_list.append(SoftwareMatchResult(unmatched_soft_pair, match_software_pair))
        if support_soft_match_list:
            return State.ASK, " ".join(self._build_warning_messages(item) for item in support_soft_match_list)
        return State.NONE, ""

    def check_selected_software(self, os_list, soft_list):
        version_matched_state, version_matched_msg = self.check_version_matched(os_list, soft_list)
        if State.EXIT == version_matched_state:
            return State.EXIT, version_matched_msg
        software_matching_state, software_matching_msg = self.check_download_software_matching(soft_list)
        if State.EXIT == software_matching_state:
            return State.EXIT, software_matching_state
        all_msg = version_matched_msg + software_matching_msg
        if State.ASK in (version_matched_state, software_matching_state):
            return State.ASK, all_msg
        return State.NONE, ""
