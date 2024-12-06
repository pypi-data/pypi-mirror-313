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
import json
import os
import re
import subprocess as sp
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_info import get_os_and_arch, need_skip_sys_package, DeployStatus
from ansible.module_utils.common_utils import ensure_docker_daemon_exist


class SysInstaller:
    def __init__(self, module, nexus_url, os_and_arch, resources_dir, pkg_type):
        self.module = module
        self.nexus_url = nexus_url
        self.os_and_arch = os_and_arch
        self.resources_dir = resources_dir
        self.stdout = []
        self.pkg_type = pkg_type
        os.environ["http_proxy"] = ""
        os.environ["https_proxy"] = ""
        os.environ["HTTP_PROXY"] = ""
        os.environ["HTTPS_PROXY"] = ""
        os.environ["LD_LIBRARY_PATH"] = ""
        with open(os.path.expanduser("~/nexus/nexus_config.json"), "r") as f:
            self.nexus_config = json.load(f)

    def create_config_file(self):
        if self.os_and_arch in self.nexus_config["rpm_os"]:
            config_content = [
                "[nexus]\n",
                "name = {}\n".format(self.os_and_arch),
                "baseurl = {}/repository/{}/\n".format(self.nexus_url, self.os_and_arch),
                "gpgcheck = 0\n",
                "enabled = 1\n",
            ]
            config_file = os.path.expanduser("~/nexus/sources.repo")
            with open(config_file, "w") as repo:
                repo.writelines(config_content)
        else:
            config_file = os.path.expanduser("~/nexus/sources.list")
            nexus_codename = self.nexus_config["codename"].get(self.os_and_arch)
            if "Debian" in self.os_and_arch:
                trusted = "[trusted=yes]"
            else:
                trusted = ""
            with open(config_file, "w") as fp:
                fp.write("deb {} {}/repository/{}/ {} main\n".format(trusted, self.nexus_url, self.os_and_arch,
                                                                     nexus_codename))

    def install_deb_pkgs(self):
        sys_pkgs = self._get_pkgs_name()
        os.environ["DEBIAN_FRONTEND"] = "noninteractive"
        os.environ["DEBIAN_PRIORITY"] = "critical"
        cmds = [
            "apt update -o Dir::Etc::sourcelist=/root/nexus/sources.list -o Dir::Etc::sourceparts='-' "
            "-o Acquire::Check-Date=false",
            "apt install -f -y -o Dir::Etc::sourcelist=/root/nexus/sources.list -o Acquire::Check-Date=false",
            "apt install -y --no-install-recommends {} -o Acquire::Check-Date=false -o "
            "Dir::Etc::sourcelist=/root/nexus/sources.list".format(sys_pkgs),
        ]
        for cmd in cmds:
            if "recommends" not in cmd:
                self._run_cmd(cmd)
            else:
                self._run_cmd(cmd, pkg_name="sys_pkg")

    def install_rpm_pkgs(self):
        self._modify_conf("enabled=1", "enabled=0")
        sys_pkgs = self._get_pkgs_name()
        cmds_pre = [
            "yum clean all",
            'yum makecache --disablerepo="*" --enablerepo=nexus -c /root/nexus/sources.repo',
        ]
        for cmd in cmds_pre:
            self._run_cmd(cmd)
        if "EulerOS" in self.os_and_arch or "CentOS" in self.os_and_arch or "Kylin_V10Lance" in self.os_and_arch:
            os_release = os.uname()[2]
            self._install_kernel(os_release, "kernel-headers")
            self._install_kernel(os_release, "kernel-devel")
        install_pkgs_cmd = (
            'yum install --skip-broken -y {} --disablerepo="*" --enablerepo=nexus '
            "-c /root/nexus/sources.repo".format(sys_pkgs)
        )
        self._run_cmd(install_pkgs_cmd, pkg_name="sys_pkg")
        self._run_cmd("systemctl restart haveged")
        self._modify_conf("enabled=0", "enabled=1")

    def install_docker(self, pkg_type="rpm"):
        if os.path.exists("/usr/bin/docker"):
            return
        if "EulerOS" in self.os_and_arch:
            docker_pkgs_name = " ".join(self.nexus_config.get("euler_docker"))
        elif "Debian" in self.os_and_arch:
            docker_pkgs_name = " ".join(self.nexus_config.get("debian_docker"))
        else:
            docker_pkgs_name = " ".join(self.nexus_config.get("common_docker"))
        if pkg_type == "rpm":
            cmd = (
                'yum install -y --skip-broken {} --disablerepo="*" --enablerepo=nexus '
                "-c /root/nexus/sources.repo".format(docker_pkgs_name)
            )
            self._run_cmd(cmd, pkg_name="docker")
        elif pkg_type == "deb":
            cmd = (
                "apt install -y --no-install-recommends {} -o Acquire::Check-Date=false -o "
                "Dir::Etc::sourcelist=/root/nexus/sources.list".format(docker_pkgs_name)
            )
            self._run_cmd(cmd, pkg_name="docker")
        self._restart_docker()

    def _modify_conf(self, pattern, repl):
        if self.os_and_arch == "BCLinux_21.10_aarch64":
            with open("/etc/dnf/plugins/license-manager.conf", "r+") as f:
                content = f.read()
                content = re.sub(pattern, repl, content)
                f.seek(0)
                f.write(content)

    def _install_kernel(self, os_release, kernel_type):
        check_kernel_headers = "rpm -q {}".format(kernel_type)
        return_code, out = self._run_cmd(check_kernel_headers, ignore_errors=True)
        kernel_version = "{}-{}".format(kernel_type, os_release)
        if return_code == 0 and out == kernel_version:
            return
        cmd = 'yum install -y {} --disablerepo="*" --enablerepo=nexus -c ' "/root/nexus/sources.repo".format(
            kernel_version
        )
        return_code, _ = self._run_cmd(cmd, ignore_errors=True)
        if return_code != 0:
            cmd = (
                'yum install -y --skip-broken {} --disablerepo="*" --enablerepo=nexus '
                "-c /root/nexus/sources.repo".format(kernel_type)
            )
            self._run_cmd(cmd)

    def _run_cmd(self, cmd, pkg_name=None, ignore_errors=False):
        rc, out, err = self.module.run_command(cmd)
        self.module.log('run_cmd: {} '.format(cmd).ljust(120, '='))
        if out:
            for line in out.splitlines():
                self.module.log(line)
        if err:
            for line in err.splitlines():
                self.module.log(line)
        if not ignore_errors and (rc != 0 or "Failed" in err):
            self.module.fail_json(msg=err, rc=1, changed=True)
        if pkg_name:
            if pkg_name == "sys_pkg":
                self.stdout.append(out)
            self.stdout.append("{} installed successfully".format(pkg_name))
        return rc, out

    def _restart_docker(self):
        return_code = sp.call(["docker", "ps"], shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
        if return_code != 0:
            self._run_cmd("systemctl daemon-reload")
            self._run_cmd("systemctl restart docker")

    def _get_pkgs_name(self):
        if "MindStudio" in self.pkg_type:
            with open(os.path.expanduser("~/nexus/{}.json".format(self.pkg_type)), "r") as f:
                pkg_info = json.load(f)
            desktop_pkg_name = []
            pkgs_name = []
            for item in pkg_info["systems"]:
                if item["system"] == self.os_and_arch:
                    for item in item["sys"]:
                        if item.get("dst_dir", "") == "desktop":
                            desktop_pkg_name.append(item.get("name"))
                        else:
                            pkgs_name.append(item.get("name"))
            if "desktop" in self.resources_dir:
                return " ".join(desktop_pkg_name)
            else:
                return " ".join(pkgs_name)
        else:
            with open(os.path.expanduser("~/nexus/pkg_info.json"), "r") as f:
                pkg_info = json.load(f)
            pkgs_name = {item.get("name") for item in pkg_info}
            docker_pkgs_name = set(self.nexus_config.get("common_docker"))
            kernel_pkgs = {"kernel-headers", "kernel-devel"}
            if "EulerOS" in self.os_and_arch:
                pkgs_name -= kernel_pkgs
                docker_pkgs_name = set(self.nexus_config.get("euler_docker"))
            elif "CentOS_7.6" in self.os_and_arch:
                pkgs_name -= kernel_pkgs
            elif "Ubuntu_22.04" in self.os_and_arch:
                pkgs_name.add("libssl-dev")
                pkgs_name.add("libssl1.1")
            return " ".join(pkgs_name - docker_pkgs_name)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            nexus_url=dict(type="str", required=True),
            ansible_run_tags=dict(type="list", required=True),
            resources_dir=dict(type="str", required=True),
            pkg_type=dict(type="str", required=True)
        )
    )
    nexus_url = module.params["nexus_url"]
    os_and_arch = get_os_and_arch()
    if need_skip_sys_package(os_and_arch):
        module.exit_json(changed=False, rc=0,
                         stdout="[ASCEND]not support installing sys_pkg on {}. Bypassing...".format(os_and_arch),
                         result={DeployStatus.DEPLOY_STATUS: DeployStatus.SKIP})
    resources_dir = os.path.expanduser(module.params["resources_dir"])
    pkg_type = module.params["pkg_type"]
    installer = SysInstaller(module, nexus_url, os_and_arch, resources_dir, pkg_type)
    installer.create_config_file()
    if "MindStudio" in module.params["pkg_type"]:
        installer.install_deb_pkgs()
        module.exit_json(changed=True, stdout="\n".join(installer.stdout), rc=0)
    else:
        if "Ubuntu" in os_and_arch or "Debian" in os_and_arch:
            installer.install_deb_pkgs()
            installer.install_docker(pkg_type="deb")
        else:
            installer.install_rpm_pkgs()
            installer.install_docker(pkg_type="rpm")
        ensure_docker_daemon_exist(module)
        module.exit_json(changed=True, stdout="\n".join(installer.stdout), rc=0)


if __name__ == "__main__":
    main()
