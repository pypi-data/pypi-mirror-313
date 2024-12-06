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
import collections
import os.path
import json
import platform
import shutil
import subprocess
import shlex
import re

from ansible.module_utils.basic import AnsibleModule


def run_command(command):
    try:
        output = subprocess.check_output(shlex.split(command))
        if not isinstance(output, str):
            output = str(output, encoding='utf-8')
        return 0, output
    except Exception as e:
        return -1, str(e)


def info_to_dict(file_path):
    """
    load info file into json. e.g.
    A = B   => {"A": "B"}
    """
    info_dict = dict()
    if not os.path.isfile(file_path):
        return info_dict
    with open(os.path.expanduser(file_path)) as fid:
        for line in fid:
            split_line = line.split("=")
            if len(split_line) == 2:
                info_dict[split_line[0].strip()] = split_line[1].strip()
    return info_dict


def get_value_on_prefix_ignore_case(_dict, _key, default=None):
    for key, value in _dict.items():
        if key.lower().startswith(_key.lower()):
            return value
    return default


def find_files(dir_path, file_name):
    targets = set()
    if not os.path.isdir(dir_path):
        return targets
    for root, _, files in os.walk(dir_path):
        if file_name in files:
            targets.add(os.path.realpath(os.path.join(root, file_name)))
    return targets


def getinfo_from_xml(file_path, root_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
    arches = {'ARM': 'aarch64', 'x86': 'x86_64'}
    info_dict = {}
    keyword_pattern = re.compile('>(.*)<')
    for line in lines:
        keyword = ""
        if keyword_pattern.findall(line):
            keyword = keyword_pattern.findall(line)[0]
        if 'OutterName' in line and keyword:
            info_dict['name'] = keyword
        if 'ProcessorArchitecture' in line and keyword:
            arch = keyword
            info_dict['install_arch'] = arches.get(arch, arch)
        if 'Version' in line and keyword:
            info_dict['version'] = keyword
    info_dict['install_path'] = root_path
    return info_dict


def get_item_info(info_dict, item):
    item_info = {}
    for key, value in info_dict.items():
        if item + "_install_path" in key.lower():
            item_version_info_path = os.path.join(value, item, "version.info")
            version_info = info_to_dict(item_version_info_path).get("Version", "")
            item_info = {"name": item, "install_arch": platform.machine(),
                         "install_path": value, "version": version_info}
    return item_info


def collect_app_info():
    info_dict = info_to_dict("/etc/ascend_install.info")
    driver_info = get_item_info(info_dict, "driver")
    firmware_info = get_item_info(info_dict, "firmware")
    apps_info = [item for item in (firmware_info, driver_info) if item]
    root_path = '/usr/local/Ascend'
    if os.getuid() != 0:
        root_path = os.path.expanduser('~/Ascend')
    for item in ['nnrt', 'toolkit', 'nnae', 'tfplugin', 'toolbox']:
        _item = item
        if item == 'toolkit':
            _item = 'ascend-toolkit'
        item_info_dir = os.path.join(root_path, _item, "latest")
        target_paths = find_files(item_info_dir, "ascend_" + item + "_install.info")
        for info_path in target_paths:
            item_info = info_to_dict(info_path)
            info_dict = {"name": item,
                         'install_path': get_value_on_prefix_ignore_case(item_info, "path", os.path.dirname(info_path)),
                         'install_arch': get_value_on_prefix_ignore_case(item_info, "arch", platform.machine()),
                         'version': get_value_on_prefix_ignore_case(item_info, "version", "")}
            apps_info.append(info_dict)
    for item in ['atlasedge', 'ha']:
        if item == 'atlasedge':
            xml_file = os.path.join("/usr/local", 'AtlasEdge/version.xml')
        else:
            xml_file = os.path.join("/usr/local", 'ha/version.xml')
        info_dict = getinfo_from_xml(xml_file, root_path)
        if info_dict:
            apps_info.append(info_dict)
    ret = {
        "progress": "1.0",
        "operation": "app display",
        "result": apps_info
    }
    return ret


def get_hccn_info():
    ret, outputs = run_command("npu-smi info -l")
    hccn_info = {}
    if not ret:
        npu_ids = []
        for line in outputs.split('\n'):
            if "NPU ID" in line:
                npu_ids.append(line.split(":")[-1].strip())
        for npu_id in npu_ids:
            hccn_lines = ""
            status, outputs = run_command("hccn_tool -i {} -ip -g".format(npu_id))
            if not status:
                hccn_lines += outputs.strip()

            status, outputs = run_command("hccn_tool -i {} -ip -inet6 -g".format(npu_id))
            if not status:
                hccn_lines += outputs.strip()

            _, outputs = run_command("hccn_tool -i {} -net_health -g".format(npu_id))
            hccn_lines += outputs.strip()

            if hccn_lines:
                hccn_info[npu_id] = hccn_lines
    return hccn_info


def get_npu_info(outputs):
    check_next_line = False
    npus = collections.defaultdict(lambda: 0)
    for line in outputs.splitlines():
        if "====" in line:
            check_next_line = True
            continue
        if check_next_line:
            words = line.split()
            if len(words) > 11:
                npus[words[2]] += 1
            check_next_line = False
    return npus


def main():
    module = AnsibleModule(argument_spec=dict(
            ip=dict(type="str", required=True),
            only_package=dict(type="bool", required=True),
        )
    )
    ip = module.params["ip"]
    only_package = module.params["only_package"]
    if os.path.exists(os.path.expanduser("~/smartkit/reports/")):
        shutil.rmtree(os.path.expanduser("~/smartkit/reports/"))
    os.makedirs(os.path.expanduser("~/smartkit/reports"))
    app_info = collect_app_info()

    if only_package:
        outputs = ["[ASCEND]{:<16} {:<16}".format("Package", "Version"), ]
        outputs.append('-' * len(outputs[-1]))
        for app in app_info.get("result", []):
            outputs.append("{:<16} {:<16}".format(app['name'], app['version']))
        return module.exit_json(changed=True, rc=0, msg="\n".join(outputs))

    with open(os.path.expanduser("~/smartkit/display.json"), 'w') as fid:
        json.dump(app_info, fid, indent=4)

    local_info = {"packages": app_info.get("result", [])}

    _, outputs = run_command("npu-smi info")
    with open(os.path.expanduser("~/smartkit/reports/driver_info.txt"), "w") as fid:
        fid.write(outputs)

    npus = get_npu_info(outputs)
    if npus:
        local_info['npu'] = ",".join(["{}:{}".format(npu_type, num) for npu_type, num in npus.items()])
    if "910" in local_info.get('npu', ''):
        hccn_info = get_hccn_info()
        if hccn_info:
            local_info['hccn'] = [value for value in hccn_info.values()]
    with open(os.path.expanduser("~/smartkit/reports/local_info.json"), "w") as fid:
        json.dump({ip: local_info}, fid, indent=4)

    module.exit_json(changed=True, rc=0)


if __name__ == "__main__":
    main()
