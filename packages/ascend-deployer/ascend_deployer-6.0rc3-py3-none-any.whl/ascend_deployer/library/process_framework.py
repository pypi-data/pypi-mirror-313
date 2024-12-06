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
import glob
import shlex
import os
import re
import subprocess as sp
import tarfile

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import common_info, common_utils
from ansible.module_utils.common_info import DeployStatus
from ansible.module_utils.common_utils import compare_version


class Installation:
    def __init__(self, module):
        self.resource_dir = os.path.expanduser(module.params["resource_dir"])
        self.pkg_name = os.path.expanduser(module.params["pkg_name"])
        self.module = module
        self.arch = common_info.ARCH
        self.messages = []
        ansible_run_tags = module.params.get("ansible_run_tags", [])
        self.is_auto_install = "auto" in ansible_run_tags
        self.python_version = self.module.params["python_version"]
        self.local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
        os.environ["PATH"] = "{}/{}/bin:".format(self.local_path, self.python_version) + os.environ["PATH"]
        os.environ["LD_LIBRARY_PATH"] = "{}/{}/lib".format(self.local_path, self.python_version)

    def run(self):
        try:
            # do install protobuf
            self.install_protobuf()
            if self.pkg_name == "mindspore":
                self.do_install_mindspore()
            elif self.pkg_name == "pytorch":
                self.do_install_pytorch()
            elif self.pkg_name == "tensorflow":
                self.do_install_tensorflow()
            else:
                self.module.fail_json(
                    msg="[ASCEND][ERROR] no pkg_name is selected.",
                    rc=1, changed=False)

            return self.module.exit_json(changed=True, rc=0, msg="\n".join(self.messages))
        except Exception as e:
            self.messages.append(str(e))
            return self.module.fail_json(changed=False, rc=1, msg="\n".join(self.messages))

    def run_command(self, command, shell=False):
        try:
            if not shell:
                command = shlex.split(command)
            process = sp.Popen(
                command,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                shell=shell,
                universal_newlines=True,
                env=os.environ
            )
            stdout, stderr = process.communicate()
            if not isinstance(stdout, str):
                stdout = str(stdout, encoding='utf-8')
            if not isinstance(stderr, str):
                stderr = str(stderr, encoding='utf-8')
            return process.returncode == 0, stdout + stderr
        except Exception as e:
            return False, str(e)

    def get_numpy_version_from_torch(self, run_file_torch):
        if "3.10." in self.python_version:
            return "1.21.3"

        numpy_version_list = {"1.11.0": "1.19.5",
                              "1.8.1": "1.19.5",
                              "2.0.1": "1.19.5",
                              "2.1.0": "1.19.5",
                              "2.2.0": "1.19.5"}
        pattern = r'torch-(.*?)-'
        match = re.search(pattern, str(run_file_torch))
        if match:
            version_string = match.group(1)
            torch_version = re.search(r"\d+\.\d+\.\d+", version_string)
            if not torch_version.group():
                return ""
        else:
            return ""
        return numpy_version_list.get(torch_version.group(), "")

    def check_install_success(self, ok, output, pkg_name):
        if ok and output:
            self.messages.append("[ASCEND] {} is installed successfully!".format(pkg_name))
        else:
            self.module.fail_json(
                msg="[ASCEND][ERROR] {} is installed failed: {}".format(pkg_name, output),
                rc=1, changed=False)

    def python_libs_install(self):
        install_messages = ["scipy==1.7.3", "cython", "pkgconfig", "requests", "sympy", "certifi", "decorator",
                            "attrs", "psutil", "pyyaml", "xlrd", "matplotlib", "grpcio",
                            "protobuf", "coverage", "gnureadline", "pylint", "absl-py", "cffi"]
        install_messages_other = ["filelock", "fsspec", "Jinja2", "MarkupSafe", "networkx", "typing_extensions==4.8.0"]
        # item = (package name - (compatiable version, python version no more support the newest package))
        # sequence is strictly defined, do not change it
        install_messages_compatiable = [('numpy', ('1.19.3', 'python3.9.0')), ('pandas', ('1.3.5', 'python3.9.0'))]
        if "3.7" not in self.python_version:
            install_messages.extend(install_messages_other)
        for package in install_messages_compatiable:
            if compare_version(self.python_version, package[1][1]) < 0:
                install_messages.insert(0, "{}=={}".format(package[0], package[1][0]))
        for lib in install_messages:
            install_command = "python3 -m pip install %s --no-index --find-links %s/pylibs" % (lib, self.resource_dir)
            ok, output = self.run_command(install_command)
            if not ok:
                self.module.fail_json(
                    msg="[ASCEND][ERROR] python libs {} is installed failed: {}".format(lib, output),
                    rc=1, changed=False)

        self.messages.append("[ASCEND] python libs is installed successfully!")

    @staticmethod
    def get_python_major_minor_version(input_string):
        """
        description: 获取python版本号和次要版本号
        """
        python_version_digits = ''.join(re.findall(r'\d+', input_string))
        version_major_minor = python_version_digits[:2]
        if version_major_minor == '31':
            version_major_minor = python_version_digits[:3]
        return version_major_minor

    def find_files(self, path, pattern):
        self.messages.append("try to find {} for {}".format(path, pattern))
        matched_files = glob.glob(os.path.join(path, pattern))
        self.messages.append("find files: " + ",".join(matched_files))
        if len(matched_files) == 1:
            return matched_files[0]
        elif len(matched_files) > 1:
            version_major_minor = self.get_python_major_minor_version(self.python_version)
            for file in matched_files:
                if "cp{}".format(version_major_minor) in file:
                    return file
            return matched_files[0]
        return None

    def check_run_file(self, run_file, pkg_name):
        msg = ("[ASCEND][ERROR] Could not find a version of {} compatible with the current Python version {}".
               format(pkg_name, self.python_version))
        # 提取 Python 版本的主要和次要版本号
        version_major_minor = self.get_python_major_minor_version(self.python_version)
        if not run_file and not self.is_auto_install:
            self.module.fail_json(
                msg="[ASCEND][ERROR] {} file not found!".format(pkg_name),
                rc=1, changed=False)
        elif not run_file and self.is_auto_install:
            self.messages.append("[ASCEND][WARNING] {} file not found!".format(pkg_name))
            self.module.exit_json(
                rc=0,
                msg="\n".join(self.messages),
                result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                changed=False)
        # 如果找到了文件，并且文件中有'cp\d+'这个结构
        elif bool(re.search(r'cp\d+', run_file)) and not self.is_auto_install:
            # cp版本和python版本不匹配的情况下
            if "cp{}".format(version_major_minor) not in run_file:
                self.module.fail_json(
                    msg=msg,
                    rc=1, changed=False)
        elif bool(re.search(r'cp\d+', run_file)) and self.is_auto_install:
            # cp版本和python版本不匹配的情况下
            if "cp{}".format(version_major_minor) not in run_file:
                self.module.exit_json(
                    msg=msg,
                    rc=0,
                    result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                    changed=False)
        return True

    def install_protobuf(self):
        local_path = "/usr/local" if os.getuid() == 0 else os.path.expanduser("~/.local")
        if glob.glob("{}/lib/libprotobuf.so.*".format(local_path)):
            return
        build_dir = os.path.join(os.path.expanduser("~"), "build")
        with tarfile.open(os.path.join(self.resource_dir, "sources/protobuf-python-3.13.0.tar.gz"), "r") as tf:
            tf.extractall(build_dir)
            for member in tf.getmembers():
                os.chown(os.path.join(build_dir, member.name), os.getuid(), os.getgid())
        cmds = ["./configure --prefix={}".format(local_path), "make -j 20", "make install"]
        os.chdir(os.path.join(build_dir, "protobuf-3.13.0"))
        for cmd in cmds:
            ok, output = self.run_command(cmd)
            if not ok or "Failed" in output:
                self.module.fail_json(
                    msg="[ASCEND][ERROR] execute {} failed: {}".format(cmd, output),
                    rc=1, changed=False)

        self.messages.append("[ASCEND] protobuf-python is installed successfully!")

    def do_install_mindspore(self):
        # check installed
        check_mindspore_cmd = 'python3 -c "import mindspore as md; print(md.__version__)"'
        ok, output = self.run_command(check_mindspore_cmd)
        if ok and output:
            self.module.exit_json(
                msg="[ASCEND] mindspore is already installed, mindspore install skipped",
                rc=0,
                result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                changed=False
            )

        # get mindspore path
        dir_name = "pylibs/Ascend"
        run_file = self.find_files(os.path.join(self.resource_dir, dir_name), r"mindspore-*-linux_%s.whl" % self.arch)
        if not self.check_run_file(run_file, "mindspore"):
            return

        # do install
        self.python_libs_install()
        command = "python3 -m pip install %s --no-index --find-links %s/pylibs" % (run_file, self.resource_dir)
        self.run_command(command)
        ok, output = self.run_command(check_mindspore_cmd)
        self.check_install_success(ok, output, "mindspore")

    def do_install_pytorch(self):
        # check installed
        check_torch_cmd = 'python3 -c "import torch; print(torch.__version__)"'
        ok, output = self.run_command(check_torch_cmd)
        if ok and output:
            self.module.exit_json(
                msg="[ASCEND] torch is already installed, torch install skipped",
                rc=0,
                result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                changed=False)
            return

        # get torch path
        dir_name = "pylibs"
        torch_path = os.path.join(self.resource_dir, dir_name)
        run_file_torch = self.find_files(torch_path, r"torch-*_%s.whl" % self.arch)
        if not self.check_run_file(run_file_torch, "torch"):
            return

        # python libs install
        self.python_libs_install()

        # get numpy path
        numpy_version = self.get_numpy_version_from_torch(run_file_torch)
        if numpy_version == "" and not self.is_auto_install:
            self.module.fail_json(
                msg="[ASCEND][ERROR] numpy_version is not found!",
                rc=1, changed=False)

        if numpy_version == "":
            self.messages.append("[ASCEND][WARNING] numpy_version is not found!")
            return

        run_file_numpy = self.find_files(torch_path, r"numpy-*%s*-*_%s.whl" % (numpy_version, self.arch))
        if not self.check_run_file(run_file_numpy, "numpy"):
            return

        # get torch_npu path
        run_file_torch_npu = self.find_files(torch_path, r"torch_npu-*_%s.whl" % self.arch)
        if not self.check_run_file(run_file_torch_npu, "torch_npu"):
            return

        # get apex path
        run_file_apex = self.find_files(torch_path, r"apex-*%s.whl" % self.arch)

        # do install apex
        if run_file_apex:
            command = "python3 -m pip install %s --no-index --find-links %s/pylibs" % (run_file_apex, self.resource_dir)
            ok, output = self.run_command(command)
            if ok:
                self.messages.append("[ASCEND] apex is installed successfully!")
            else:
                self.module.fail_json(
                    msg="[ASCEND][ERROR] apex is installed failed: {}".format(output),
                    rc=1, changed=False)

        # do install numpy
        check_numpy_cmd = 'python3 -c "import numpy; print(numpy.__version__)"'
        command = "python3 -m pip install %s --no-index --find-links %s/pylibs" % (run_file_numpy, self.resource_dir)
        self.run_command(command)
        ok, output = self.run_command(check_numpy_cmd)
        self.check_install_success(ok, output, "numpy")

        # do install torch
        command = "python3 -m pip install %s --no-index --find-links %s/pylibs" % (run_file_torch, self.resource_dir)
        self.run_command(command)
        ok, output = self.run_command(check_torch_cmd)
        self.check_install_success(ok, output, "torch")

        # do install torch_npu
        check_torch_npu_cmd = 'python3 -c "import torch_npu; print(torch_npu.__version__)"'
        command = "python3 -m pip install %s --no-index --find-links %s/pylibs" % (
            run_file_torch_npu, self.resource_dir)
        self.run_command(command)
        ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
        source_env_cmd = ". %s/ascend-toolkit/set_env.sh" % ascend_install_path
        toolkit_path = "{}/ascend-toolkit/set_env.sh".format(ascend_install_path)
        if not os.path.exists(toolkit_path):
            source_env_cmd = ". %s/nnae/set_env.sh" % ascend_install_path
        commands = [source_env_cmd, check_torch_npu_cmd]
        ok, output = self.run_command(" && ".join(commands), shell=True)
        self.check_install_success(ok, output, "torch_npu")

    def do_install_tensorflow(self):
        # check installed
        check_tensorflow_cmd = 'python3 -c "import tensorflow as tf; print(tf.__version__)"'
        ok, output = self.run_command(check_tensorflow_cmd)
        if ok and output:
            self.module.exit_json(
                msg="[ASCEND] tensorflow is already installed, tensorflow install skipped",
                rc=0,
                result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP},
                changed=False)
            return

        # get tensorflow path
        dir_name = "pylibs"
        run_file = self.find_files(os.path.join(self.resource_dir, dir_name), r"tensorflow*_%s.whl" % self.arch)
        install_tensorflow = "tensorflow"
        if run_file and "tensorflow_cpu" in run_file:
            install_tensorflow = "tensorflow_cpu"
        if not self.check_run_file(run_file, install_tensorflow):
            return

        # do install
        command = "python3 -m pip install %s --no-index --find-links %s/pylibs" % (
            install_tensorflow, self.resource_dir)
        self.run_command(command)
        ok, output = self.run_command(check_tensorflow_cmd)
        self.check_install_success(ok, output, "tensorflow")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            resource_dir=dict(type="str", required=True),
            pkg_name=dict(type="str", required=True),
            python_version=dict(type="str", required=True),
            ansible_run_tags=dict(type="list", required=True)
        )
    )
    Installation(module).run()


if __name__ == "__main__":
    main()
