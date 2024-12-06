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
import shutil

from ansible.module_utils.basic import AnsibleModule


class GccInstaller:
    MAJOR_VERSION = 7
    SUB_VERSION = 3

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                resources_dir=dict(type="str", required=True),
            )
        )
        self.resources_dir = os.path.expanduser(self.module.params["resources_dir"])
        self.gcc_name = "gcc-7.3.0"
        self.build_dir = self.create_build_dir()
        self.gcc_dir = os.path.join(self.build_dir, self.gcc_name)
        self.local_path = "/usr/local"

    @staticmethod
    def create_build_dir():
        build_dir = "{}/build".format(os.path.expanduser("~"))
        if not os.path.isdir(build_dir):
            os.makedirs(build_dir, mode=0o750)
        return build_dir

    def run_cmd(self, cmd):
        result = sp.Popen(
            shlex.split(cmd),
            shell=False,
            universal_newlines=True,
            stderr=sp.PIPE,
            stdout=sp.PIPE,
        )
        out, err = result.communicate()
        if result.returncode != 0:
            return self.module.fail_json(msg=err, rc=1, changed=True)
        return out

    def is_need_install_gcc(self):
        if not self.module.get_bin_path("gcc"):
            return True
        cmd = "gcc --version"
        out = self.run_cmd(cmd)
        if not out:
            return True
        ver_info = out.splitlines()[0].split()
        if len(ver_info) < 3:
            return True
        version = ver_info[2]
        major, sub, _ = version.split(".")
        if not major.isdigit() or not sub.isdigit():
            return True
        if int(major) < self.MAJOR_VERSION:
            return True
        elif int(major) == self.MAJOR_VERSION and int(sub) < self.SUB_VERSION:
            return True
        return False

    def unarchive_gcc(self):
        tar_cmd = "tar --no-same-owner -xf {}/sources/{}.tar.gz -C {}".format(
            self.resources_dir, self.gcc_name, self.build_dir
        )
        self.run_cmd(tar_cmd)

    def copy_package(self, package):
        shutil.copy("{}/sources/{}".format(self.resources_dir, package), self.gcc_dir)

    def install_gcc(self):
        os.chdir(self.gcc_dir)
        # make distclean
        if os.path.exists(os.path.join(self.gcc_dir, "Makefile")):
            cmd = "make -C {} distclean".format(self.gcc_dir)
            self.run_cmd(cmd)

        self.run_cmd("bash contrib/download_prerequisites")

        config_gcc_cmd = ("./configure --enable-languages=c,c++ --disable-multilib --with-system-zlib --prefix={}/{}"
                          " --disable-stage1-checking --disable-libgcj").format(self.local_path, self.gcc_name)
        self.run_cmd(config_gcc_cmd)
        self.run_cmd("make -C {} -j20".format(self.gcc_dir))
        self.run_cmd("make -C {} install".format(self.gcc_dir))
        # 创建软连接
        self.run_cmd("ln -sf {} /usr/bin/gcc".format(os.path.join(self.local_path, "gcc-7.3.0/bin/gcc")))


def main():
    installer = GccInstaller()
    if not installer.is_need_install_gcc():
        return installer.module.exit_json(changed=False, rc=0, msg="gcc version is satisfied, skip install gcc.")
    # 准备安装包
    installer.unarchive_gcc()
    installer.copy_package("mpfr-3.1.4.tar.bz2")
    installer.copy_package("mpc-1.0.3.tar.gz")
    installer.copy_package("gmp-6.1.0.tar.bz2")
    installer.copy_package("isl-0.16.1.tar.bz2")
    # 安装gcc
    installer.install_gcc()
    return installer.module.exit_json(changed=True, rc=0)


if __name__ == "__main__":
    main()
