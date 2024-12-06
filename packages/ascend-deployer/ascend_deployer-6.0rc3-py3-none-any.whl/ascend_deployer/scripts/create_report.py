#!/usr/bin/env python3
# coding: utf-8
# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
import glob
import json
import os
import sys
import csv

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


def solve_value_list(value_list):
    res_iter = (item.get("name", "") + ":" + item.get("version", "") for item in value_list if isinstance(item, dict))
    return "\n".join(res_iter)


def get_hccn(hccn_list):
    if not hccn_list:
        return 'NA'
    for hccn in hccn_list:
        if isinstance(hccn, str) and 'success' not in hccn.lower():
            return 'fail'
    return 'ok'


def write_csv(merged_data, dir_name):
    ips = list(merged_data.keys())

    field_names = ["IP", "Node name", "Node type", "Node status", "Npu numbers", "Software package version",
                   "HCCN health check", "Running pods", "MindX-DL status"]
    flags = os.O_WRONLY | os.O_CREAT
    with os.fdopen(os.open(dir_name + '/report.csv', flags, 0o644), 'w') as wf:
        writer = csv.DictWriter(wf, fieldnames=field_names)
        writer.writeheader()
        for ip in ips:
            row = [ip]
            npu = merged_data.get(ip, {}).get('npu', 'NA')
            packages = solve_value_list(merged_data.get(ip, {}).get('packages', []))
            hccn_list = merged_data.get(ip, {}).get('hccn', [])
            hccn_info = get_hccn(hccn_list)
            node_name = merged_data.get(ip, {}).get('node name', 'NA')
            node_type = merged_data.get(ip, {}).get('node type', 'NA')
            status = merged_data.get(ip, {}).get('status', 'NA')
            ready_pods = "\n".join(merged_data.get(ip, {}).get('ready pods', []))
            result = merged_data.get(ip, {}).get('dl result', 'NA')
            row.extend(
                [node_name, node_type, status, npu, packages or 'NA', hccn_info, ready_pods or 'NA',
                 result or 'NA'])
            writer.writerow(dict(zip(field_names, row)))


def main(jsons_path, output_path, inventory_file_path):
    inventory = InventoryManager(loader=DataLoader(), sources=[inventory_file_path, ])
    workers = inventory.get_hosts(pattern='worker')
    masters = inventory.get_hosts(pattern='master')
    all_hosts = set(workers + masters)

    json_files = []
    for parent, _, files in os.walk(jsons_path):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(parent, file))
    merged_data = {}
    localhost_data = {}
    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            for ip in data.keys():
                data_value = data.get(ip, {})
                if ip == 'localhost':
                    localhost_data.update(data_value)
                    continue
                merged_data.setdefault(ip, {}).update(data_value)
    if localhost_data and len(merged_data) == 0:
        merged_data['localhost'] = localhost_data

    for host in all_hosts:
        if str(host) not in merged_data and str(host) != 'localhost':
            merged_data[str(host)] = {}

    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    with os.fdopen(os.open(output_path + '/report.json', flags, 0o644), 'w') as f:
        json.dump(merged_data, f)

    write_csv(merged_data, output_path)


if __name__ == '__main__':
    from_path = sys.argv[1]
    to_path = sys.argv[2]
    inventory_file = sys.argv[3]
    main(from_path, to_path, inventory_file)
