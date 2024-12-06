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
import os
import json
import platform
import tarfile
import shlex
import re

from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.common_info import get_os_and_arch

VERSION_PATTERN = re.compile(r"(\d+)")


# same as the function in ~/utils.py, do not delete it cuz need to be imported in ansible
def compare_version(src_version, target_version):
    use_version_parts = VERSION_PATTERN.split(src_version)
    new_version_parts = VERSION_PATTERN.split(target_version)
    for cur_ver_part, new_ver_part in zip(use_version_parts, new_version_parts):
        if cur_ver_part.isdigit() and new_ver_part.isdigit():
            result = int(cur_ver_part) - int(new_ver_part)
        else:
            result = (cur_ver_part > new_ver_part) - (cur_ver_part < new_ver_part)
        if result != 0:
            return result
    return len(use_version_parts) - len(new_version_parts)


def get(module, url):
    resp, info = fetch_url(module, url, method='GET', use_proxy=False)
    try:
        content = resp.read()
    except AttributeError:
        content = info.pop('body', '')
    return to_text(content, encoding='utf-8')


def get_protocol(module, host):
    https_url = 'https://{}/c/login'.format(host)
    content = get(module, https_url)
    if 'Not Found' in content:
        return 'https'
    if 'wrong version number' in content:
        return 'http'

    http_url = 'http://{}/c/login'.format(host)
    content = get(module, http_url)
    if 'The plain HTTP request was sent to HTTPS port' in content:
        return 'https'
    return 'http'


def clean_env():
    for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
        os.environ.pop(key, None)


def ensure_docker_daemon_exist(module):
    docker_daemon = "/etc/docker/daemon.json"
    if os.path.exists(docker_daemon):
        return
    content_dict = dict()
    rpm = module.get_bin_path('rpm')
    if not rpm:
        content_dict.update({
            "exec-opts": ["native.cgroupdriver=systemd"],
            "live-restore": True
        })
    elif get_os_and_arch().startswith('OpenEuler'):
        content_dict.update({
            "live-restore": True
        })
    docker_config_path = os.path.dirname(docker_daemon)
    if not os.path.exists(docker_config_path):
        os.makedirs(docker_config_path, mode=0o750)
    with open(docker_daemon, 'w') as f:
        json.dump(content_dict, f, indent=4)
    module.run_command('systemctl daemon-reload')
    module.run_command('systemctl restart docker')


def find_files(path, pattern):
    messages = ["try to find {} for {}".format(path, pattern)]
    matched_files = glob.glob(os.path.join(path, pattern))
    messages.append("find files: " + ",".join(matched_files))
    return matched_files, messages


def run_command(module, command, ok_returns=None, working_dir=None):
    messages = ["calling " + command]
    return_code, out, err = module.run_command(shlex.split(command), cwd=working_dir)
    output = out + err
    if not ok_returns:
        ok_returns = [0]
    if return_code not in ok_returns:
        raise Exception("calling {} failed on {}: {}".format(command, return_code, output))
    messages.append("output of " + command + " is: " + str(output))
    return output, messages


def result_handler(failed_msg=""):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                res, msgs = func(self, *args, **kwargs)
                self.messages.extend(msgs)
            except Exception as e:
                self.messages.append(failed_msg)
                raise e
            if not res:
                raise Exception(failed_msg)

            return res

        return wrapper

    return decorator


def get_cmd_color_str(s, color):
    # 定义颜色对应的 ANSI 转义序列
    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    # 获取对应的颜色代码，如果颜色不存在则直接返回原始字符串
    if color not in colors:
        return s

    # 返回带颜色的字符串
    return "{}{}{}".format(colors[color], s, colors['reset'])


def generate_table(result, title, columns, header_name):
    # 获取实际存在的列
    actual_columns = [col for col in columns if any(col in data for data in result.values())]

    # 如果没有实际存在的列，返回空字符串
    if not actual_columns:
        return ""

    # 构建表头
    header = [header_name] + actual_columns
    table = [header]

    # 构建表格
    for worker, data in result.items():
        if any(col in data for col in actual_columns):
            row = [worker] + ["{}, {}".format(data.get(col, ["", ""])[0], data.get(col, ["", ""])[1]).strip(", ")
                              for col in actual_columns]
            table.append(row)

    # 如果表格只有表头，返回空字符串
    if len(table) == 1:
        return ""

    # 计算每一列的最大宽度
    col_widths = [max(len(str(item)) for item in col) for col in zip(*table)]

    # 构建格式化字符串
    format_str = " | ".join(["{{:<{}}}".format(width) for width in col_widths])

    # 构建分割线
    separator = "-+-".join(["-" * width for width in col_widths])

    # 将表格转换为字符串
    table_str = title + "\n" + separator + "\n" + "\n".join(
        [format_str.format(*row) for row in table[:1]]) + "\n" + separator + "\n" + "\n".join(
        [format_str.format(*row) for row in table[1:]]) + "\n" + separator

    # 利用shell标签增加颜色
    table_str = table_str.replace("not installed", get_cmd_color_str("not installed", 'yellow'))
    table_str = table_str.replace("OK", get_cmd_color_str("OK", 'green'))
    table_str = table_str.replace("ERROR", get_cmd_color_str("ERROR", 'red'))

    return table_str