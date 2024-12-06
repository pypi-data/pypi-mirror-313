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
import glob
import os
import platform
import shlex
import subprocess as sp
import tarfile

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_info import DeployStatus, get_os_and_arch
from ansible.module_utils.check_utils import CheckUtil


class CANNInstaller:
    _scene_card_map = {
        "a300i":    "310p",
        "a300iduo": "310p",
        "train":    "910",
        "a910b":    "910b",
        "a910_93":  "910_93"
    }

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                python_version=dict(type="str", required=True),
                run_tags=dict(type="list", required=True),
                resources_dir=dict(type="str", required=True),
                pkg_name=dict(type="str", required=True),
                npu_info=dict(type="dict", required=True),
                log_file_name=dict(type="str", required=False),
                action=dict(type="str", required=False, default="install"),
                is_ipv6=dict(type="bool", required=False, default=False),
            )
        )
        self.python_version = self.module.params["python_version"]
        self.run_tags = self.module.params["run_tags"]
        self.resources_dir = os.path.expanduser(self.module.params["resources_dir"])
        self.cann_dir = os.path.join(self.resources_dir, "run_from_cann_zip")
        self.pkg_name = self.module.params["pkg_name"]
        self.npu_info = self.module.params["npu_info"]
        self.log_file_name = self.module.params['log_file_name']
        self.is_ipv6 = self.module.params["is_ipv6"]
        self.action = self.module.params["action"]
        self.uid = os.getuid()
        self.build_dir = os.path.expanduser("~/build")
        self.log_path = "/var/log/ascend_seclog/"
        self.local_path = "/usr/local"
        self.cann_install_params = "--install --quiet --install-for-all"
        self.ascend_install_path = "/usr/local/Ascend"
        self.stdout = []
        os.environ["PATH"] = "{}/{}/bin:".format(self.local_path, self.python_version) + os.environ.get("PATH", "")
        os.environ["LD_LIBRARY_PATH"] = "{}/{}/lib".format(self.local_path, self.python_version)

    def install_pkg(self):
        script = self._get_install_script()
        if self.action == "patch":
            return self._install_patch(script)
        if self.action == "rollback":
            return self._patch_rollback(script)
        model = self.npu_info["model"]
        scene = self.npu_info["scene"]
        install_cmd = self._get_install_cmd(script, scene, model)
        return self._run_install_pkg(install_cmd)

    def _get_install_cmd(self, script, scene, model):
        if script.endswith(".sh"):
            install_cmd = "/bin/bash {} {}".format(script, self.log_path)
            if self.pkg_name == "kernels":
                install_cmd += " {}".format(self._get_kernels_type(script, scene))
            return install_cmd
        install_cmd = "/bin/bash {} --nox11 ".format(script)
        if self.pkg_name == "toolbox" and model == "Atlas 200I SoC A1":
            os.environ["TOOLBOX_SOC"] = "A200ISoC"
            install_cmd += "--install-type=A200ISoC "
        if self.pkg_name == "kernels":
            install_cmd += "--type={}".format(self._get_kernels_type(script, scene))
        info_path = "{}/*/latest/ascend_{}_install.info".format(self.ascend_install_path, self.pkg_name)
        if self.pkg_name == "toolkit" or self.pkg_name == "nnrt":
            info_path = "{}/*/latest/*/ascend_{}_install.info".format(self.ascend_install_path, self.pkg_name)
        if glob.glob(info_path):
            install_cmd += "--upgrade --quiet"
            return install_cmd
        install_cmd = "{} {}".format(install_cmd, self.cann_install_params)
        return install_cmd

    def _install_patch(self, script):
        install_params = "--nox11 --install --quiet"
        install_cmd = "/bin/bash {} {}".format(script, install_params)
        self._run_cmd(install_cmd, input_="y")
        return self.module.exit_json(stdout="\n".join(self.stdout), rc=0, changed=True)

    def _patch_rollback(self, script):
        rollback_cmd = "/bin/bash {} --rollback".format(script)
        self._run_cmd(rollback_cmd, input_="y")
        return self.module.exit_json(stdout="\n".join(self.stdout), rc=0, changed=True)

    def _build_mpi_and_hccl_test(self):
        if not os.path.exists("{}/ascend-toolkit/latest/tools/hccl_test".format(self.ascend_install_path)):
            self.stdout.append("[ASCEND]can not find hccl_test folder, compile mpi and hccl_test skipped")
            return
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir, 0o700)
        mpi_path = self._find_mpi_path()
        toolkit_path = os.path.dirname(
            os.path.dirname(
                os.path.realpath("{}/ascend-toolkit/latest/tools/hccl_test".format(self.ascend_install_path))
            )
        )
        with tarfile.open(mpi_path, "r") as tf:
            tf.extractall(self.build_dir)
            gid = os.getgid()
            for member in tf.getmembers():
                os.chown(os.path.join(self.build_dir, member.name), self.uid, gid)
        os.chdir(os.path.join(self.build_dir, os.path.basename(mpi_path).strip(".tar.gz")))
        config_mpi_cmd = "./configure --prefix={}/mpi --disable-fortran".format(self.local_path)
        self._run_cmd(config_mpi_cmd, no_log=True)
        self._run_cmd("make -j 40", no_log=True)
        self._run_cmd("make install", pkg_name="mpi", no_log=True)
        os.chdir("{}/tools/hccl_test".format(toolkit_path))
        os.environ["PATH"] = "{}/mpi/bin:".format(self.build_dir) + os.environ.get("PATH", "")
        os.environ["LD_LIBRARY_PATH"] = "{0}/runtime/lib64:{0}/runtime/lib64/stub:{0}/compiler/lib64:{1}".format(
            toolkit_path, os.environ.get("LD_LIBRARY_PATH", "")
        )
        compile_hccl_cmd = "make MPI_HOME={}/mpi ASCEND_DIR={}".format(self.local_path, toolkit_path)
        self._run_cmd(compile_hccl_cmd, pkg_name="hccl_test", no_log=True)

    def _find_mpi_path(self):
        scene = self.npu_info["scene"]
        if self.is_ipv6:
            mpi_path_pattern = "{}/sources/openmpi*.tar.gz"
        elif scene == "a910_93":
            mpi_path_pattern = "{}/sources/mpich-4*.tar.gz"
        else:
            mpi_path_pattern = "{}/sources/mpich-3*.tar.gz"
        mpi_path_search = glob.glob(mpi_path_pattern.format(self.resources_dir))
        if mpi_path_search:
            return mpi_path_search[0]
        else:
            self.module.fail_json(changed=False, rc=1,
                                  msg=("[ASCEND]can not find the mpi package, "
                                       "Ensure that the mpi package is in the {}/sources directory.".format(
                                        self.resources_dir)))

    def _check_pkg(self, install_script):
        if install_script:
            return
        elif self.pkg_name in self.run_tags:
            return self.module.fail_json(
                changed=False,
                rc=1,
                msg=(
                    "[ASCEND]failed to install the {0} because the {0} package cannot be found. "
                    "Ensure that the {0} package is in the {1} directory.".format(self.pkg_name, self.cann_dir)
                ),
            )
        else:
            return self.module.exit_json(
                stdout="[ASCEND]can not find {0} package, {0} install skipped".format(self.pkg_name),
                result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                rc=0,
                changed=False,
            )

    def _get_install_script(self):
        def get_script(script_type):
            scene = self.npu_info["scene"]
            arch = platform.machine()
            pkg_list = glob.glob("{}/*{}*{}.{}".format(self.cann_dir, self.pkg_name, arch, script_type))
            if self.pkg_name == "kernels":
                card = self._scene_card_map.get(scene, "--")
                self.log_file_name = self.log_file_name + card + '_install.log'
                if scene == "a910_93":
                    # 优先根据架构查找，未找到执行or后面的语句
                    pkg_list = (
                            glob.glob("{}/Atlas-A3*{}_*{}.{}".format(self.cann_dir, self.pkg_name, arch, script_type))
                            or glob.glob("{}/Atlas-A3*{}_*.{}".format(self.cann_dir, self.pkg_name, script_type))
                    )
                else:
                    pkg_list = (
                            glob.glob("{}/*{}-{}_*{}.{}".format(self.cann_dir, self.pkg_name, card, arch, script_type))
                            or glob.glob("{}/*{}-{}_*.{}".format(self.cann_dir, self.pkg_name, card, script_type))
                    )
            return pkg_list

        if self.action in ("patch", "rollback"):
            script = get_script("run")
        else:
            script = get_script("sh") or get_script("run")

        self._check_pkg(script)
        return script[0]

    def _run_install_pkg(self, cmd):
        self._run_cmd(cmd, input_="y")
        if self.pkg_name == "toolkit":
            self._build_mpi_and_hccl_test()
        return self.module.exit_json(stdout="\n".join(self.stdout), rc=0, changed=True)

    def _get_last_error_log(self):
        max_reverse_num = 20
        log_path = os.path.join(self.log_path, self.log_file_name)
        cover_msg = 'please check the log file {} to see the details'.format(log_path)
        if not os.path.exists(log_path):
            return cover_msg
        error_str = 'ERROR'
        reverse_error = error_str[::-1]
        with open(log_path, 'rb') as log_file:
            log_file.seek(0, os.SEEK_END)
            pos = log_file.tell()
            line = ''
            line_num = 0
            while pos >= 0:
                log_file.seek(pos)
                pos -= 1
                try:
                    new_char = log_file.read(1).decode('utf-8')
                    if new_char == '\n' and line_num <= max_reverse_num:
                        line_num += 1
                        if reverse_error in line:
                            return '.'.join([line[::-1], cover_msg])  # 倒序输出
                        line = ''
                    else:
                        line += new_char
                except UnicodeDecodeError as e:
                    continue
            if reverse_error in line:  # 第一行容错
                return line[::-1]
        return cover_msg

    def _run_cmd(self, cmd, input_=None, pkg_name="", no_log=False):
        result = sp.Popen(
            shlex.split(cmd),
            shell=False,
            universal_newlines=True,
            stderr=sp.PIPE,
            stdin=sp.PIPE,
            stdout=sp.PIPE,
        )
        out, err = result.communicate(input=input_)
        if result.returncode != 0:
            if not err or len(err) == 0:
                err = self._get_last_error_log()
            return self.module.fail_json(msg=err, rc=1, changed=True)
        if pkg_name:
            self.stdout.append("build {} success".format(pkg_name))
        if not no_log:
            self.stdout.append(out)

    def _get_kernels_type(self, script, scene):
        if scene == "infer" and "kernels" not in self.run_tags:
            return self.module.exit_json(
                stdout="[ASCEND]kernels not support infer scene, kernels install skipped",
                result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                rc=0, changed=True
            )
        script_name_split = os.path.basename(script).split("_")
        index = 1
        kernels_version = script_name_split[index] if len(script_name_split) > index else None
        if not kernels_version:
            return self.module.fail_json(
                changed=False,
                rc=1,
                msg=(
                    "[ASCEND]cann not find version from name {}, please check.".format(os.path.basename(script))
                ),
            )
        if glob.glob("{}/*/{}/ascend_{}_install.info".format(self.ascend_install_path, kernels_version, "nnae")):
            return "nnae"
        elif glob.glob("{}/*/{}/*/ascend_{}_install.info".format(self.ascend_install_path, kernels_version, "toolkit")):
            return "toolkit"
        return ""


def main():
    installer = CANNInstaller()
    installer.install_pkg()


if __name__ == "__main__":
    main()
