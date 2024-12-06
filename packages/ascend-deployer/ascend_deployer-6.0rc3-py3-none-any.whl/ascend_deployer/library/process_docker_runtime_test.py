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
import subprocess
import json

from ansible.module_utils.basic import AnsibleModule

OK = "OK"
ERROR = "ERROR"


def run_command(command, custom_env=None):
    try:
        env = os.environ.copy()
        if custom_env:
            env.update(custom_env)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True, env=env, executable="/bin/bash")
        stdout, stderr = process.communicate()
        if not isinstance(stdout, str):
            stdout = str(stdout, encoding='utf-8')
        if not isinstance(stderr, str):
            stderr = str(stderr, encoding='utf-8')
        return process.returncode == 0, stdout + stderr
    except Exception as e:
        return False, str(e)


def test_ascend_docker_runtime():
    """
    description: 查看Ascend Docker Runtime组件状态，Ascend Docker Runtime只在worker节点安装
    """
    # step1.查看default runtime 字段是否为ascend
    ok, output = run_command('docker info')
    if not ok or 'Default Runtime: ascend' not in output:
        return 'not installed', ''
    # step2.查看daemon.json文件
    try:
        with open('/etc/docker/daemon.json', 'r') as file:
            docker_daemon = json.load(file)
        if docker_daemon.get('default-runtime') != 'ascend' or 'ascend' not in docker_daemon.get('runtimes'):
            return ERROR, ''
        parsed_dict = {}
        with open('/usr/local/Ascend/Ascend-Docker-Runtime/ascend_docker_runtime_install.info', 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    parsed_dict[key.strip()] = value.strip()
    except FileNotFoundError:
        return ERROR, ''
    return OK, parsed_dict.get('version')


def main():
    """
    description: 在检查worker节点检查ascend-docker-runtime组件状态
    """
    module = AnsibleModule(argument_spec=dict(
            ansible_run_tags=dict(type="list", required=True),
            node_name=dict(type="str", required=True),
        )
    )
    ansible_run_tags = set(module.params["ansible_run_tags"])
    if 'whole' in ansible_run_tags:
        ansible_run_tags = ['ascend-docker-runtime']

    result = {}
    if module.params["node_name"]:
        host_name = module.params["node_name"]
    else:
        ok, output = run_command('hostname')
        if ok:
            host_name = output.strip()
        else:
            host_name = ' '

    # 在worker中检测ascend-docker-runtime组件
    if "ascend-docker-runtime" in ansible_run_tags:
        result = {
            host_name: {"ascend-docker-runtime": test_ascend_docker_runtime()}
        }

    return module.exit_json(changed=True, rc=0, result=result, msg="")


if __name__ == "__main__":
    main()