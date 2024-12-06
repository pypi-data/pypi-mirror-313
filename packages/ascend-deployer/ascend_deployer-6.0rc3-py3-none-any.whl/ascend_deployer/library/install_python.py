#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
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
import shlex
import subprocess as sp

from ansible.module_utils.basic import AnsibleModule


class PythonInstaller:
    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                resources_dir=dict(type="str", required=True),
                python_tar=dict(type="str", required=True),
                os_and_arch=dict(type="str", required=True),
            )
        )
        self.resources_dir = os.path.expanduser(self.module.params["resources_dir"])
        self.os_and_arch = self.module.params["os_and_arch"]
        self.python_tar = self.module.params["python_tar"]
        self.python_version = self.python_tar.replace("P", "p").replace("-", "")
        self.build_dir = self.create_build_dir()
        self.local_path = "/usr/local"
        self.pip_install_option = ""

    @staticmethod
    def create_build_dir():
        build_dir = "{}/build".format(os.path.expanduser("~"))
        try:
            os.makedirs(build_dir, mode=0o750)
        except OSError:
            pass
        return build_dir

    def run_cmd(self, cmd):
        result = sp.Popen(
            shlex.split(cmd),
            shell=False,
            universal_newlines=True,
            stderr=sp.PIPE,
            stdout=sp.PIPE,
        )
        _, err = result.communicate()
        if result.returncode != 0:
            return self.module.fail_json(msg=err, rc=1, changed=True)
        return ""

    def unarchive_python(self):
        tar_cmd = "tar --no-same-owner -xf {}/sources/{}.tar.xz -C {}".format(
            self.resources_dir, self.python_tar, self.build_dir
        )
        self.run_cmd(tar_cmd)

    def install_python(self):
        os.chdir(os.path.join(self.build_dir, self.python_tar))
        config_python_cmd = "./configure --enable-shared --prefix={}/{}".format(self.local_path, self.python_version)
        if "CentOS_7.6" in self.os_and_arch:
            config_python_cmd += " --with-openssl=/usr/local/openssl11"
        self.run_cmd(config_python_cmd)
        self.run_cmd("make -j 20")
        self.run_cmd("make install")

    def install_python_libs(self):
        os.environ["PATH"] = "{}/{}/bin:".format(self.local_path, self.python_version) + os.environ["PATH"]
        os.environ["LD_LIBRARY_PATH"] = "{}/{}/lib".format(self.local_path, self.python_version)
        install_pip_cmd = "python3 -m pip"
        sp.call(shlex.split(install_pip_cmd), shell=False)
        upgrade_pip_cmd = "python3 -m pip install --upgrade pip --no-index --find-links {}/pylibs {}".format(
            self.resources_dir, self.pip_install_option
        )
        sp.call(shlex.split(upgrade_pip_cmd), shell=False)
        if "EulerOS" in self.os_and_arch:
            install_selinux_cmd = "python3 -m pip install selinux --no-index --find-links {}/pylibs {}".format(
                self.resources_dir, self.pip_install_option
            )
            sp.call(shlex.split(install_selinux_cmd), shell=False)

    def create_ascendrc(self):
        with os.fdopen(
            os.open("{}/ascendrc".format(self.local_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o640), "w"
        ) as f:
            content = [
                "export PATH={}/{}/bin:$PATH".format(self.local_path, self.python_version),
                "export LD_LIBRARY_PATH={}/{}/lib:$LD_LIBRARY_PATH".format(self.local_path, self.python_version),
                "",
            ]
            f.writelines("\n".join(content))


def main():
    installer = PythonInstaller()
    installer.unarchive_python()
    installer.install_python()
    installer.install_python_libs()
    installer.create_ascendrc()
    installer.module.exit_json(changed=True, rc=0)


if __name__ == "__main__":
    main()
