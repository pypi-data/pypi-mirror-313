#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
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
import json
import os
from typing import List

from .download_util import get_arch, get_specified_python
from .software_mgr import SoftwareMgr, SoftwareVersion

_PYTHON_MAPPING = {
    "Python-3.7": "cp37",
    "Python-3.8": "cp38",
    "Python-3.9": "cp39",
    "Python-3.10": "cp310",
    "Python-3.11": "cp311"
}

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(CUR_DIR)


class DownloadData:

    def __init__(self, selected_os_list, selected_soft_list, dst=""):
        self.software_mgr = SoftwareMgr()
        self.selected_os_list = selected_os_list
        self.selected_soft_list = selected_soft_list
        self.selected_soft_ver_list = self._parse_software_list(self.software_mgr, selected_soft_list)
        self.base_dir = dst if dst else PROJECT_DIR
        self.resources_dir = os.path.join(self.base_dir, 'resources')
        self.arch = get_arch(selected_os_list)
        self.specified_python = get_specified_python()
        self.py_implement_flag = self._get_py_implement_flag(self.specified_python)

    @staticmethod
    def _parse_software_list(software_mgr: SoftwareMgr, software_list: List[str]) -> List[SoftwareVersion]:
        return [SoftwareVersion(*software_mgr.get_software_name_version(software)) for software in software_list]

    @staticmethod
    def _get_py_implement_flag(specified_python):
        py_iter = (cp_ver for py_ver, cp_ver in _PYTHON_MAPPING.items() if py_ver in specified_python)
        implement_flag = next(py_iter, "cp37")
        return implement_flag
