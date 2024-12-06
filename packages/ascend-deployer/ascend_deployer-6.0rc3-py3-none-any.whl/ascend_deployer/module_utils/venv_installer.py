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
import os.path
import shutil

from ansible.module_utils import common_utils


class VenvInstaller(object):
    _WAIT_TIME = 60

    def __init__(self, module, venv_dir, pylibs_dir, python_dir, pkg_cmd=""):
        self.module = module
        self.venv_dir = venv_dir
        self.pylibs_dir = pylibs_dir
        self.python_dir = python_dir
        self.pkg_cmd = pkg_cmd
        self.venv_pip_path = os.path.join(venv_dir, "bin", "pip3")

    def create_venv_dir(self):
        if os.path.exists(self.venv_dir):
            shutil.rmtree(self.venv_dir)
        return common_utils.run_command(self.module, "python3 -m venv {}".format(self.venv_dir))

    def update_pip(self):
        cmd = "{} install --upgrade pip --no-index --find-links {}".format(self.venv_pip_path, self.pylibs_dir)
        return common_utils.run_command(self.module, cmd)

    def install_pkg(self, pkg):
        cmd = "{} install {} --no-index --find-links {}".format(self.venv_pip_path, pkg, self.pylibs_dir)
        return common_utils.run_command(self.module, cmd)

    def create_link(self):
        if not self.pkg_cmd:
            return
        source = os.path.join(self.venv_dir, "bin", self.pkg_cmd)
        target = os.path.join(self.python_dir, "bin")
        if not target:
            raise Exception("Target path not existed: {}.".format(target))
        shutil.copy(source, target)
