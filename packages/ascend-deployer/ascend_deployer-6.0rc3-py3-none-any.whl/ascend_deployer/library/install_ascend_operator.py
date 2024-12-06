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

from ansible.module_utils.dl import Installer


class AscendOperatorInstaller(Installer):
    component_name = 'ascend-operator'

    def clear_previous_namespace(self):
        self.module.run_command("kubectl delete clusterrolebinding ascend-operator-rolebinding")
        self.module.run_command("kubectl delete sa ascend-operator")
        self.module.run_command("kubectl delete clusterrole pods-ascend-operator-role")
        self.module.run_command("kubectl delete deploy ascend-operator")


if __name__ == '__main__':
    AscendOperatorInstaller().run()
