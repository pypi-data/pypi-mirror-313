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
from .software_mgr import PkgInfo

LOG = logger_config.LOG


class DlComponentDownloader:
    DELETE = "Delete"
    UPDATE = "Update"

    def __init__(self, download_data: DownloadData):
        """
        eg:
        _software_list ['DL==6.0.RC2']
        _os_list ['Ubuntu_20.04_x86_64']
        """
        self._download_data = download_data
        self._software_mgr = download_data.software_mgr
        self._software_list = download_data.selected_soft_list
        self._os_list = download_data.selected_os_list

    @staticmethod
    def _get_pkg_info_from_json(resources_json, arch) -> List[PkgInfo]:
        with open(resources_json, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            data = json_data.get(arch, [])
        return [PkgInfo(**item) for item in data]

    def _update_or_del_pkg(self, pkg_list: List[PkgInfo], pkg: PkgInfo) -> List[PkgInfo]:
        """
        Delete or update COMMON pkg based on COMMON_UPDATE json configuration.
        :param pkg_list: the list of origin PkgInfo from COMMON
        :param pkg: PkgInfo from COMMON_UPDATE
        :eg. {
             "filename": "aarch64.tar.gz",
             "dest": "resources/docker/OpenEuler_20.03_LTS",
             "remark": "Update"
           }
        :return: PkgInfo list
        """
        if pkg.remark == self.DELETE:
            return [p for p in pkg_list if not (p.filename == pkg.filename and p.dest == pkg.dest)]
        elif pkg.remark == self.UPDATE:
            return [p for p in pkg_list if not (p.filename == pkg.filename and p.dest == pkg.dest)] + [pkg]
        else:
            return pkg_list + [pkg]

    def _has_dl(self):
        for soft in self._download_data.selected_soft_list:
            if "DL" in soft:
                return True
        return False

    def collect_dl_contents_dependency(self):
        result = []
        if not self._has_dl():
            return result
        download_dl = any("DL" in pkg_name for pkg_name in self._software_list)
        download_aarch64 = any("aarch64" in os_item for os_item in self._os_list)
        download_x86_64 = any("x86_64" in os_item for os_item in self._os_list)
        software_with_version_list = [self._software_mgr.get_name_version(item, std_out=False) for item in
                                      self._software_list]
        dl_version = ""
        for pkg_name in software_with_version_list:
            if "DL" in pkg_name and "_" in pkg_name:
                dl_version = pkg_name.split("_")[1]
        pkg_info_list: List[PkgInfo] = []
        for arch, is_download in (('aarch64', download_aarch64), ('x86_64', download_x86_64)):
            if not is_download:
                continue
            if download_dl:
                resources_json = os.path.join(self._download_data.base_dir,
                                              f'downloader/software/DL_{dl_version}.json')
                pkg_info_list.extend(self._get_pkg_info_from_json(resources_json, arch))
        for pkg in pkg_info_list:
            print(f"analysis results: filename: {pkg.filename}")
            dest_file_path = os.path.join(self._download_data.base_dir, pkg.dest, pkg.filename)
            result.append(DownloadFileInfo(filename=pkg.filename, url=pkg.url, sha256=pkg.sha256,
                                           dst_file_path=dest_file_path))
            LOG.info(f'{pkg.filename} download from {pkg.url}')
        return result
