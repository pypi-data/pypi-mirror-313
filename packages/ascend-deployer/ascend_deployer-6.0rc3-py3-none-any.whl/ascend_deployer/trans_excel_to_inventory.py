#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
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
import csv
import ipaddress
import os
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FILE_NAME = 'inventory_template.csv'
NEED_HCCN_VARS = False


def get_data():
    """Retrieves data from a CSV file."""
    hccn_data = []
    workers_data = []
    table_header = []
    hccn_vars_date = []
    csv_file_path = get_csv_path()
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if 'HCCN' == row[0].strip():
                hccn_data.append(row)
                if not hccn_vars_date:
                    hccn_vars_date = row
            elif 'worker' == row[0].strip():
                workers_data.append(row)
                if not hccn_vars_date:
                    hccn_vars_date = row
            elif 'IP' in row and 'ansible_ssh_user' in row:
                table_header.extend(row)
    logging.info("Start data processing...")
    if hccn_data:
        global NEED_HCCN_VARS
        NEED_HCCN_VARS = True
    return hccn_data, workers_data, table_header, hccn_vars_date


def get_csv_path():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, FILE_NAME)
    return file_path


def is_valid_ip(ip_cidr):  # Check if the input string is a valid IP address or IP network.
    try:
        ipaddress.ip_address(ip_cidr)
        return True
    except ValueError:
        try:
            ipaddress.ip_network(ip_cidr)
            return True
        except ValueError:
            pass
    return False


def get_node_ip(nodes_list):
    if len(nodes_list) not in (8, 16):
        raise Exception(f"Please confirm the number of nodes is correct.The number of nodes should be \
        eight or sixteen.{nodes_list}")
    if all(nodes_list) or (all(nodes_list[:8]) and not any(nodes_list[8:])):
        nodes = ''
        for node in nodes_list:
            if is_valid_ip(node):
                nodes += node + ','
            elif node.strip() == '':
                pass
            else:
                raise ValueError(f"invalid node IP address: {node}")
        return nodes.strip(',')
    raise Exception(f"Please confirm the number of nodes is correct.The number of nodes should be \
    eight or sixteen.{nodes_list}")


def get_gateways(gateways_list):
    if gateways_list == ['']:
        return ''
    for gateway in gateways_list:
        gateway = gateway.strip()
        if is_valid_ip(gateway):
            continue
        else:
            raise ValueError(f"invalid gateway address: {gateway}")
    return ','.join(gateways_list)


def valid_netmask(netmask):
    if not netmask:
        return True
    try:
        # Check for IPv4 netmask
        ipaddress.IPv4Network(f"0.0.0.0/{netmask}", strict=False)
        return True
    except ValueError:
        if isinstance(netmask, int):  # Check for IPv6 netmask
            if 0 <= netmask <= 128:
                return True
        return False


def check_bitmap(lst):
    if lst == ['']:
        return True
    count_0 = lst.count('0')
    count_1 = lst.count('1')
    if count_0 == 7 and count_1 == 1 and len(lst) == 8:
        return True
    if count_0 == 15 and count_1 == 1 and len(lst) == 16:
        return True
    return False


def check_dscp_tc(dscp_tc_str):
    if not dscp_tc_str:
        return True
    pattern = r'^\d{1,2}:\d{1},'
    match = re.match(pattern, dscp_tc_str)
    if not match:
        return False
    dscp_tc_str = dscp_tc_str.strip(',')
    dscp, tc = map(int, dscp_tc_str.split(':'))
    return 0 <= dscp <= 63 and 0 <= tc <= 7


def check_common_network(common_network_str):
    if not common_network_str:
        return True
    elif common_network_str == "0.0.0.0/0":
        return True
    return False


def get_hccn_vars(data_list, data_header):
    gateways_index = data_header.index('gateways')
    netmask_index = data_header.index('netmask')
    bitmap_index = data_header.index('bitmap')
    dscp_tc_index = data_header.index('dscp_tc')
    common_network_index = data_header.index('common_network')
    gateways_list = data_list[gateways_index].strip().split(',')
    gateways = get_gateways(gateways_list)
    netmask = data_list[netmask_index].strip()
    if not gateways and NEED_HCCN_VARS:
        raise Exception(f"Please fill in the gateways information of the HCCN")
    if not netmask and NEED_HCCN_VARS:
        raise Exception(f"Please fill in the netmask information of the HCCN")
    if not valid_netmask(netmask):
        raise ValueError(f"invalid netmask: {netmask}")
    bitmap = data_list[bitmap_index].strip()
    if not check_bitmap(bitmap.split(',')):
        raise ValueError(f"invalid bitmap: {bitmap}")
    dscp_tc = data_list[dscp_tc_index].strip()
    if not check_dscp_tc(dscp_tc):
        raise ValueError(f"invalid dscp_tc: {dscp_tc}")
    common_network = data_list[common_network_index].strip()
    if not check_common_network(common_network):
        raise ValueError(f"invalid common_network: {common_network}")
    return {"gateways": gateways, "netmask": netmask, "bitmap": bitmap, "dscp_tc": dscp_tc,
            "common_network": common_network}


def get_user_info(item, data_header):
    user = []
    ip_index = data_header.index('IP')
    ssh_user_index = data_header.index('ansible_ssh_user')
    ssh_pass_index = data_header.index('ansible_ssh_pass')
    user_ip = item[ip_index].strip()
    if is_valid_ip(user_ip):
        user.append(user_ip)
    else:
        raise ValueError(f"invalid IP address: {user_ip}")
    ssh_user = item[ssh_user_index].strip()
    if not ssh_user:
        raise Exception(f"Please fill in the ansible_ssh_user information of the IP:{user_ip}")
    ssh_pass = item[ssh_pass_index]
    if ssh_pass:
        user.extend([f"ansible_ssh_user='{ssh_user}'", f"ansible_ssh_pass='{ssh_pass}'"])
    else:
        user.extend([f"ansible_ssh_user='{ssh_user}'"])
    return user


def get_hccn(data_list, data_header):
    hccn_info = []
    node_index = data_header.index('NPU0')
    detect_ip_index = data_header.index('NPU0', node_index + 1)
    for item in data_list:
        user = get_user_info(item, data_header)
        device_ip = get_node_ip(item[node_index:node_index + 16])
        detect_ip = get_node_ip(item[detect_ip_index:detect_ip_index + 16])
        user.extend([f"deviceip={device_ip}", f"detectip={detect_ip}"])
        hccn_info.append(' '.join(user))
    return hccn_info


def get_workers(data_list, data_header):
    workers_info = []
    for item in data_list:
        user = get_user_info(item, data_header)
        workers_info.append(' '.join(user))
    return workers_info


def write_inventory(hccn, hccn_vars, workers):
    all_vars = {
        "SCALE": "false",
        "RUNNER_IP": ""
    }
    # data write to inventory_file
    with open('inventory_file', mode='w', encoding='utf-8') as file:
        # write hccn information
        file.write('[hccn]\n')
        for item in hccn:
            file.write(item + '\n')
        # write hccn：vars information
        file.write('\n[hccn:vars]\n')
        for key, value in hccn_vars.items():
            file.write(f'{key}="{value}"\n')
        file.write('roce_port=4791\n')
        # write master information
        file.write('\n[master]\n')
        # write worker information
        file.write('\n[worker]\n')
        file.write("localhost ansible_connection='local' ansible_ssh_user='root'\n")
        for worker in workers:
            file.write(worker + '\n')
        # write other_build_image information
        file.write('\n[other_build_image]\n')
        # write all_vars information
        file.write('\n[all:vars]\n')
        for key, value in all_vars.items():
            file.write(f'{key}="{value}"\n')
    logging.info("Data has been written to the inventory_file successfully.")


if __name__ == '__main__':
    hccn_list, worker_list, head_list, hccn_vars_list = get_data()
    hccn_config = get_hccn(hccn_list, head_list)
    hccn_vars_config = get_hccn_vars(hccn_vars_list, head_list)
    workers_config = get_workers(worker_list, head_list)
    write_inventory(hccn_config, hccn_vars_config, workers_config)
