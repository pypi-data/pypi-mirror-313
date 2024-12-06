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
import os
import re
import shutil

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import common_info, common_utils, venv_installer
from ansible.module_utils.common_utils import result_handler, compare_version
from ansible.module_utils.common_info import DeployStatus


class FaultDiagInstaller(object):

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                resources_dir=dict(type="str", required=True),
                ansible_run_tags=dict(type="list", required=True),
                python_version=dict(type="str", required=True),
            )
        )
        self.resources_dir = os.path.expanduser(self.module.params["resources_dir"])
        self.arch = common_info.ARCH
        self.local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
        self.ascend_install_path = os.path.join(self.local_path, "Ascend")
        self.dist_tmp_dir = os.path.join(self.ascend_install_path, "dist_tmp_dir")
        self.ansible_run_tags = self.module.params.get("ansible_run_tags", [])
        self.python_version = self.module.params["python_version"]
        self.python_path = os.path.join(self.local_path, self.python_version)
        self.venv_dir = os.path.join(self.ascend_install_path, "faultdiag")
        self.pylibs_dir = os.path.join(self.resources_dir, "pylibs")
        self.messages = []

    def _module_failed(self):
        return self.module.fail_json(msg="\n".join(self.messages), rc=1, changed=False)

    def _module_success(self):
        return self.module.exit_json(msg="Install Fault Diag success.", rc=0, changed=True)

    @result_handler(failed_msg="Not found python from expected python path. Please install python by ascend-deployer.")
    def _check_python(self):
        return os.path.exists(self.python_path), ["Expected python path: {}".format(self.python_path)]

    def _add_python_env(self):
        os.environ["PATH"] = "{}/bin:".format(self.python_path) + os.environ["PATH"]
        os.environ["LD_LIBRARY_PATH"] = "{}/lib".format(self.python_path)

    @staticmethod
    def extract_digits(input_string):
        """
        description: 仅保留并返回字符串中的数字
        """
        return ''.join(re.findall(r'\d+', input_string))

    def _find_fd_pkg(self):
        pattern = "*faultdiag*{}.whl".format(self.arch)
        pkgs, msgs = common_utils.find_files(os.path.join(self.resources_dir, "FaultDiag"), pattern)
        self.messages.extend(msgs)
        if not pkgs:
            if "auto" in self.ansible_run_tags:
                self.module.exit_json(std_out="[ASCEND]can not find faultdiag package, faultdiag install skipped", rc=0,
                                      result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                                      changed=False)
            else:
                self.messages.append("[ASCEND]can not find faultdiag package.")
                self._module_failed()
        if len(pkgs) == 1:
            return pkgs[0]
        else:
            # 提取 Python 版本的主要和次要版本号
            python_version_digits = self.extract_digits(self.python_version)
            version_major_minor = python_version_digits[:2]
            if version_major_minor == '31':
                version_major_minor = python_version_digits[:3]
            # 查找与 Python 版本匹配的文件
            for pkg in pkgs:
                if 'py3' in pkg and compare_version(self.python_version, 'python3.7.0') >= 0:
                    return pkg
                if "cp{}".format(version_major_minor) in pkg:
                    return pkg
            # 如果没有和当前python匹配的文件
            std_out = ("[ASCEND][ERROR] Could not find a version of fault-diag "
                       "compatible with the current Python version {}".format(self.python_version))
            if "auto" in self.ansible_run_tags:
                self.module.exit_json(std_out=std_out, rc=0,
                                      result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                                      changed=False)
            else:
                self.messages.append(std_out)
                self._module_failed()

    def _generate_installer(self):
        installer = venv_installer.VenvInstaller(module=self.module, venv_dir=self.venv_dir,
                                                 pylibs_dir=self.pylibs_dir,
                                                 python_dir=self.python_path, pkg_cmd="ascend-fd")
        return installer

    @result_handler(failed_msg="Failed to install ascend-fd.")
    def _install_fd(self, installer, pkg):
        return installer.install_pkg(pkg)

    @staticmethod
    def _install_pkgs(installer, pkgs):
        all_msg = []
        for pkg in pkgs:
            try:
                output, msg = installer.install_pkg(pkg)
                all_msg.extend(msg)
            except Exception as e:
                all_msg.append(str(e))
                all_msg.append("[ERROR]Install {} failed!".format(pkg))
                return False, all_msg
        return True, all_msg

    @result_handler(failed_msg="Failed to install required packages.")
    def _install_required_pkgs(self, installer):
        if compare_version(self.python_version, 'python3.8.0') >= 0:
            return self._install_pkgs(installer, ["importlib.resources", "pyinstaller"])
        py37_libs = ["numpy==1.21.6", "scipy==1.7.3", "scikit_learn==1.0.2", "pandas==1.3.5", "pyinstaller==5.13.2"]
        return self._install_pkgs(installer, py37_libs)

    @result_handler(failed_msg="Failed to show ascend-faultdiag info.")
    def _show_ascend_fd_info(self, venv_pip_path):
        return common_utils.run_command(self.module, "{} show ascend-faultdiag".format(venv_pip_path))

    @result_handler(failed_msg="Failed to show ascend-faultdiag info.")
    def _find_fd_site_package_dir(self, venv_pip_path):
        res = self._show_ascend_fd_info(venv_pip_path)
        match = re.search(r"Location: (.+)", res)
        if match:
            return match.group(1), []
        return "", []

    @result_handler(failed_msg="Failed to create binary ascend-fd.")
    def _create_binary_file(self):
        venv_bin_dir = os.path.join(self.venv_dir, "bin")
        pyinstall_path = os.path.join(venv_bin_dir, "pyinstaller")
        ascend_fd_path = os.path.join(venv_bin_dir, "ascend-fd")
        venv_pip_path = os.path.join(venv_bin_dir, "pip3")
        fd_install_dir = self._find_fd_site_package_dir(venv_pip_path)
        if not os.path.exists(self.dist_tmp_dir):
            os.makedirs(self.dist_tmp_dir)
        cmd = """
        {} --onefile {} \
        --hidden-import=ascend_fd \
        --hidden-import=pandas \
        --hidden-import=numpy \
        --hidden-import=sklearn \
        --hidden-import=ply \
        --hidden-import=ply.lex \
        --hidden-import=ply.yacc \
        --hidden-import=prettytable \
        --hidden-import=ipaddress \
        --hidden-import=importlib.resources \
        --add-data "{}/ascend_fd:ascend_fd" \
        --distpath={} \
        --name="ascend-fd"
        """.format(pyinstall_path, ascend_fd_path, fd_install_dir, self.dist_tmp_dir)
        return common_utils.run_command(self.module, cmd)

    def _copy_binary_to_usr_local_bin(self):
        binary_path = os.path.join(self.dist_tmp_dir, "ascend-fd")
        target_path = os.path.realpath("/usr/local/bin/ascend-fd")
        shutil.copy(binary_path, target_path)
        # 授予所有用户执行权限
        os.chmod(target_path, 0o755)

    @result_handler(failed_msg="Install ascend-fd failed.")
    def _check_fd_existed(self):
        return common_utils.run_command(self.module, "ascend-fd version")

    def _clear(self):
        shutil.rmtree(self.dist_tmp_dir)
        shutil.rmtree(self.venv_dir)

    def run(self):
        pkg = self._find_fd_pkg()
        installer = self._generate_installer()
        try:
            self._check_python()
            self._add_python_env()
            installer.create_venv_dir()
            installer.update_pip()
            self._install_required_pkgs(installer)
            self._install_fd(installer, pkg)
            self._create_binary_file()
            self._copy_binary_to_usr_local_bin()
            self._check_fd_existed()
            self._clear()
        except BaseException as e:
            self.messages.append(str(e))
            self._module_failed()
        self._module_success()


def main():
    FaultDiagInstaller().run()


if __name__ == "__main__":
    main()
