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
from html.parser import HTMLParser
from typing import List, Dict

import urllib.parse

from . import logger_config
from .download_util import CONFIG_INST, DOWNLOAD_INST, get_specified_python
from .software_mgr import PylibInfo

__all__ = ('LinkParser', 'Package', 'Pip', 'download', 'pip')

DOWNLOADER_PATH = os.path.dirname(__file__)
LOG = logger_config.LOG
UNIQUE_PYTHON_DEPENDENCIES = {
    "cp310": list(map(PylibInfo.parse_line,
                      ["matplotlib==3.7.1", "pandas==2.0.3", "cycler==0.11.0", "kiwisolver==1.3.2", "numpy==1.21.3",
                       "Pillow==8.3.2", "setuptools_scm==4.1.1", "cppy==1.2.0", "pybind11==2.6.1", "scipy==1.7.2",
                       "contourpy==1.0.1", "fonttools==4.22.1"]))
}


class LinkParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = {}
        self.last_link = {}

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        self.last_link = urllib.parse.urljoin(self.base_url, dict(attrs).get('href'))

    def handle_data(self, data):
        if self.lasttag != 'a':
            return
        self.links[data] = self.last_link


class Package(object):
    def __init__(self, name, version, url, style, filename, cp='', abi='', arch=''):
        self.name = name
        self.version = version
        self.url = url
        self.style = style
        self.filename = filename
        self.cp = cp
        self.abi = abi
        self.arch = arch

    def __str__(self):
        return f'Package(name={self.name}, version={self.version}, style={self.style}, cp={self.cp}, ' \
               f'abi={self.abi}, arch={self.arch})'

    def __repr__(self):
        return str(self)

    @classmethod
    def parse_source(cls, tar_name, pkg, version, url):
        pkg_name, ver = tar_name.replace('.tar.gz', '').replace('.zip', '').rsplit('-', 1)
        if ver == version:
            return cls(pkg, version, url, 'source', tar_name)
        return None

    @classmethod
    def parse_wheel(cls, whl_name, pkg, version, url):
        pkg_name, ver, cp, abi, arch = whl_name.rstrip('.whl').rsplit('-', 4)
        if ver == version:
            return cls(pkg, version, url, 'wheel', whl_name, cp, abi, arch)
        return None

    @classmethod
    def parse(cls, name, pkg, version, url):
        if name.endswith(('.tar.gz', '.zip')):
            return cls.parse_source(name, pkg, version, url)
        elif name.endswith('.whl'):
            return cls.parse_wheel(name, pkg, version, url)
        else:
            return None

    def download(self, save_dir):
        file_path = os.path.join(save_dir, self.filename)
        DOWNLOAD_INST.download(self.url, file_path)
        print(f"analysis results: filename: {self.filename}, version: {self.version}")
        LOG.info(f'download {self.filename} successfully')


class Pip(object):
    arch_map = {
        'x86_64': ('linux_x86_64', 'manylinux1_x86_64', 'manylinux2010_x86_64', 'manylinux2014_x86_64', 'any'),
        'aarch64': ('linux_aarch64', 'manylinux_2_17_aarch64', 'manylinux2014_aarch64', 'any')
    }

    def __init__(self, pypi_url: str, link_cache: Dict[str, str] = None):
        self.cache = {}
        self.pypi_url = pypi_url
        self.url_cache = link_cache or {}

    def filter(self, link_pkgs: List[Package], pylib_info: PylibInfo, arch: str) -> List[Package]:
        """
        available pkgs must meet below requirements:
            1.whl(or):
                1. pkg.abi == abi3 and pkg.abi <= target_cp
                2. pkg.arch match target arch
            2.source
        choice order:
            1. whl > source
            2. pkg.filename
        """
        results = []
        available_cp_set = {pylib_info.cp, 'py{}'.format(pylib_info.cp[2:3])}
        for pkg in link_pkgs:
            if pkg.cp:
                if pkg.abi == 'abi3':
                    cps = [int(x.strip('cp')) for x in pkg.cp.split('.')]
                    target_cp = int(pylib_info.cp.strip('cp'))
                    if pkg.cp.startswith('cp') and not any(filter(lambda x: x <= target_cp, cps)):
                        continue
                elif not (set(pkg.cp.split('.')) & available_cp_set):
                    continue
            if pkg.arch and not (set(pkg.arch.split('.')) & set(self.arch_map.get(arch, []))):
                continue
            results.append(pkg)
        results.sort(key=lambda x: (x.style, x.filename), reverse=True)
        return results

    def update_cache_url(self, pkg_name: str, links: Dict[str, str]):
        for name, link in self.url_cache.items():
            if pkg_name in name:
                links[name] = link
                LOG.info('update {} link to {}'.format(name, link))

    def get_links(self, pkg_name: str):
        dist_name = pkg_name.lower()
        if dist_name not in self.cache:
            if not self.pypi_url.endswith('/'):
                self.pypi_url += '/'
            dist_url = urllib.parse.urljoin(self.pypi_url, dist_name + '/')
            print(f"Getting available download packages from {dist_url}")
            res_buffer = DOWNLOAD_INST.urlopen(dist_url)
            parser = LinkParser(dist_url)
            parser.feed(res_buffer.decode())
            self.update_cache_url(pkg_name, parser.links)
            self.cache[dist_name] = parser.links
            LOG.info(f'save {pkg_name}({dist_name}) links to cache')
        return self.cache.get(dist_name)

    def filter_pkg(self, links: Dict[str, str], pylib_info: PylibInfo, arch: str) -> Package:
        choices = []
        for name, link in links.items():
            pkg = Package.parse(name, pylib_info.name, pylib_info.version, link)
            if pkg:
                choices.append(pkg)
        filter_choices = self.filter(choices, pylib_info, arch)
        if filter_choices:
            LOG.info(f'for {pylib_info.name}=={pylib_info.version}, '
                     f'available choices: {[p.filename for p in filter_choices]}')
            return filter_choices[0]
        LOG.error(f'no available package found for {pylib_info.name}=={pylib_info.version}')

    def download_pkg(self, save_dir: str, pylib_info: PylibInfo, arch: str):
        links = self.get_links(pylib_info.name)
        pkg = self.filter_pkg(links, pylib_info, arch)
        if not pkg:
            raise Exception(f'no available package found for {pylib_info.name}')
        pkg.download(save_dir)


with open(os.path.join(DOWNLOADER_PATH, 'obs_resources.json')) as cache_file:
    url_cache = json.load(cache_file)
pip = Pip(CONFIG_INST.get_pypi_url(), link_cache=url_cache)


def _parse_cp():
    specified_python = get_specified_python() or ""
    specified_python = specified_python.replace('Python-', 'cp')
    return ''.join(specified_python.split('.')[:2])


def _query_arches(os_list):
    arches = set()
    for os_item in os_list:
        if 'x86_64' in os_item:
            arches.add('x86_64')
        else:
            arches.add('aarch64')
    return arches


def _read_ansible_reqs() -> List[PylibInfo]:
    ansible_require_file = os.path.join(DOWNLOADER_PATH, 'ansible_reqs.json')
    with open(ansible_require_file) as f:
        reqs = json.load(f)
        res = []
        for cp, lines in reqs.items():
            for line in lines:
                pylib_info = PylibInfo.parse_line(line)
                pylib_info.cp = cp
                res.append(pylib_info)
        return res


def _download_ansible_reqs(arches, save_dir):
    for pylib_info in _read_ansible_reqs():
        for arch in arches:
            pip.download_pkg(save_dir, pylib_info, arch)


def _read_requirements() -> List[PylibInfo]:
    require_file = os.path.join(DOWNLOADER_PATH, 'requirements.txt')
    with open(require_file) as f:
        return [PylibInfo.parse_line(str(line)) for line in f.readlines()]


def _download_requirements(arches, save_dir):
    cp = _parse_cp()
    requirements_pylibs = _read_requirements() + UNIQUE_PYTHON_DEPENDENCIES.get(cp, [])
    for pylib_info in requirements_pylibs:
        pylib_info.cp = cp
        for arch in arches:
            pip.download_pkg(save_dir, pylib_info, arch)


def _check_pypi_connectivity():
    check_url = pip.pypi_url if pip.pypi_url.endswith('/') else pip.pypi_url + '/'
    check_url = urllib.parse.urljoin(check_url, "cython" + "/")

    DOWNLOAD_INST.urlopen(check_url)


def download(os_list, res_dir):
    """download ansible and requirement base on os_list"""
    print("Start analyzing Python dependency packages...")
    # check pypi base URL
    _check_pypi_connectivity()
    arches = _query_arches(os_list)
    save_dir = os.path.join(res_dir, 'pylibs')
    print("Start analyzing the required py packages for ansible...")
    _download_ansible_reqs(arches, save_dir)
    print("Start analyzing the required Py packages for the project...")
    _download_requirements(arches, save_dir)
