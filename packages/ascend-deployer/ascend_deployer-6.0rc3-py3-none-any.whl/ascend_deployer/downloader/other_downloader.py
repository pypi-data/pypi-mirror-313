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

import json
import os
from typing import List

from . import logger_config
from .download_data import DownloadData
from .parallel_file_downloader import DownloadFileInfo
from .software_mgr import PkgInfo, SoftwareVersion

LOG = logger_config.LOG
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(CUR_DIR)


class OtherDownloader:
    _AI_FRAMES = ("MindSpore", "Torch-npu", "TensorFlow")

    def __init__(self, download_data: DownloadData):
        self._download_data = download_data
        self._arch = download_data.arch
        self._software_list = download_data.selected_soft_list
        self._selected_soft_ver_list = download_data.selected_soft_ver_list
        self._base_dir = download_data.base_dir
        self._software_mgr = download_data.software_mgr
        self._non_ai_frame_list = [soft_ver for soft_ver in self._selected_soft_ver_list if
                                   not self._is_ai_frame(soft_ver)]
        self._ai_frame_list = [soft_ver for soft_ver in self._selected_soft_ver_list if self._is_ai_frame(soft_ver)]
        self.warning_message = set()

    @staticmethod
    def _is_ai_frame(soft_ver: SoftwareVersion):
        return any(soft in soft_ver.name for soft in OtherDownloader._AI_FRAMES)

    @staticmethod
    def _unsupported_arch_mind_studio_file(filename, arch):
        return "MindStudio" in filename \
            and ("x86_64" in filename or "aarch64" in filename) \
            and isinstance(arch, str) \
            and arch not in filename

    @staticmethod
    def _mk_download_dir(other_pkgs: List[PkgInfo], download_dir, software):
        if any(not pkg.dest for pkg in other_pkgs):
            if not os.path.exists(download_dir):
                os.makedirs(download_dir, mode=0o750, exist_ok=True)
            LOG.info('item:{} save dir: {}'.format(software, os.path.basename(download_dir)))

    @staticmethod
    def _collect_pkgs_by_arch(arch, download_dir, dst, other_pkgs) -> List[DownloadFileInfo]:
        if arch == "x86_64" or arch == "aarch64":
            other_pkgs = (item for item in other_pkgs if arch in item.filename.replace("-", "_")
                          or ("kernels" in item.filename and not any(
                arch in item.filename for arch in ["x86_64", "aarch64"])))
        file_list = []
        for item in other_pkgs:
            if item.dest:
                dest_file = os.path.join(dst, item.dest, item.filename)
            else:
                dest_file = os.path.join(download_dir, item.filename)

            print(f"analysis results: filename: {item.filename}")
            file_list.append(
                DownloadFileInfo(filename=item.filename, url=item.url, sha256=item.sha256, dst_file_path=dest_file))
            LOG.info(f'{item.filename} download from {item.url}')
        return file_list

    def _collect_download_software(self, soft_ver: SoftwareVersion, arch) -> List[DownloadFileInfo]:
        """
        下载软件的其他资源
        """
        other_pkgs = self._software_mgr.get_software_other(soft_ver.name, soft_ver.version)
        other_pkgs = [pkg for pkg in other_pkgs if
                      not self._unsupported_arch_mind_studio_file(pkg.filename, self._arch)]
        if "CANN" in soft_ver.name and "3.10." in self._download_data.specified_python:
            other_pkgs = [pkg for pkg in other_pkgs if "tfplugin" not in pkg.filename]
        download_dir = os.path.join(self._base_dir, "resources", "{0}_{1}".format(soft_ver.name, soft_ver.version))
        self._mk_download_dir(other_pkgs, download_dir, soft_ver)
        if soft_ver.name in ("CANN", "NPU", "FaultDiag"):
            results = self._collect_pkgs_by_arch(arch, download_dir, self._base_dir, other_pkgs)
        else:
            results = []
            for item in other_pkgs:
                print(f"analysis results: filename: {item.filename}")
                results.append(DownloadFileInfo(filename=item.filename, url=item.url, sha256=item.sha256,
                                        dst_file_path=os.path.join(download_dir, item.filename)))
                LOG.info(f'{item.filename} download from {item.url}')
        return results

    def collect_other_software(self):
        """
        按软件列表下载其他部分
        """
        result = []
        for soft_ver in self._non_ai_frame_list:
            result.extend(self._collect_download_software(soft_ver, self._arch))
        return result

    @staticmethod
    def _get_target_pkg_list(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return [PkgInfo(**item) for item in data]

    def _is_need_download_file(self, filename):
        return "nexus" not in filename or not isinstance(self._arch, str) or self._arch in filename

    def collect_other_pkgs(self) -> List[DownloadFileInfo]:
        other_pkgs = self._get_target_pkg_list(os.path.join(CUR_DIR, 'other_resources.json'))
        need_download_other_pkgs = [pkg for pkg in other_pkgs if self._is_need_download_file(pkg.filename)]
        res = []
        for pkg in need_download_other_pkgs:
            print(f"analysis results: filename: {pkg.filename}")
            res.append(DownloadFileInfo(filename=pkg.filename, url=pkg.url, sha256=pkg.sha256,
                                 dst_file_path=os.path.join(self._base_dir, pkg.dest, pkg.filename)))
            LOG.info(f'{pkg.filename} download from {pkg.url}')
        return res

    def collect_specified_python(self) -> List[DownloadFileInfo]:
        pkg_list = self._get_target_pkg_list(os.path.join(CUR_DIR, 'python_version.json'))
        res = []
        for pkg in pkg_list:
            if self._download_data.specified_python == pkg.filename.rstrip('.tar.xz'):
                print(f"analysis results: filename: {pkg.filename}")
                res.append(DownloadFileInfo(filename=pkg.filename, url=pkg.url, sha256=pkg.sha256,
                                            dst_file_path=os.path.join(self._base_dir, pkg.dest, pkg.filename)))
                LOG.info(f'{pkg.filename} download from {pkg.url}')
        return res

    def _collect_framework_whl(self, os_item, soft_ver: SoftwareVersion):
        download_dir = os.path.join(self._base_dir, "resources")
        os_item_split = os_item.split("_")
        os_name, arch = "_".join(os_item_split[:2]), "_".join(os_item_split[2:])
        whl_list = self._software_mgr.get_software_framework(soft_ver.name, "linux_{}".format(arch), soft_ver.version)
        result = []
        for item in whl_list:
            if item.python != self._download_data.py_implement_flag:
                continue
            dest_file = os.path.join(download_dir, item.dest, os.path.basename(item.url))
            print(f"analysis results: filename: {item.filename}")
            result.append(
                DownloadFileInfo(filename=item.filename, url=item.url, sha256=item.sha256, dst_file_path=dest_file))
            LOG.info(f'{item.filename} download from {item.url}')
        if not result:
            self.warning_message.add("[ASCEND][WARNING]: No {} {} found for {} on {}, skipping...".format(
                soft_ver.name, soft_ver.version, self._download_data.specified_python, arch))
        return result

    def collect_ai_framework(self):
        result = []
        for os_item in self._download_data.selected_os_list:
            for framework_soft_ver in self._ai_frame_list:
                result.extend(self._collect_framework_whl(os_item, framework_soft_ver))
        return result
