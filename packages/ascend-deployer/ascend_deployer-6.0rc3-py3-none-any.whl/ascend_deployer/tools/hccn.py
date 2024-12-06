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
import os
import re
import subprocess
import sys
import socket

IP_RULE_TEMPLATE = "ip_rule_%s=add from %s table %s\n"
IP_ROUTE_TEMPLATE = "ip_route_%s=add %s via %s dev eth%s table %s\n"
ADDRESS_TEMPLATE = """address_%s=%s
netmask_%s=%s
netdetect_%s=%s
"""
IPV6_ADDRESS_TEMPLATE = """IPv6address_%s=%s
IPv6netmask_%s=%s
IPv6netdetect_%s=%s
"""
ROCE_PORT_TEMPLATE = "roce_port_%s=%s\n"
ARP_SEND_TEMPLATE = "send_arp_status_%s=%s\n"
DSCP_TC_TEMPLATE = "dscp_tc_%s=%s\n"
BITMAP_TEMPLATE = "bitmap_%s=%s\n"

GATEWAY_TEMPLATE = "gateway_%s=%s\n"
IPV6_GATEWAY_TEMPLATE = "IPv6gateway_%s=%s\n"
ARP_TEMPLATE = "arp_%s=-i eth%s -s %s %s\n"

RET_ERROR_CODE = 127
FIRST_CARD_IN_SECOND_GROUP = 4
FIRST_GROUP = (0, 1, 2, 3)
SECOND_GROUP = (4, 5, 6, 7)


def is_ipv6(address):
    return ":" in address


def is_same_ipv6_subnet(ip1, ip2, subnet_mask):
    try:
        truncated_ip1 = get_ipv6_subnet(ip1, subnet_mask)
        truncated_ip2 = get_ipv6_subnet(ip2, subnet_mask)
        return truncated_ip1 == truncated_ip2
    except Exception:
        print("Invalid IPv6 address or subnet mask")
        return False


def get_ipv6_subnet(ip, subnet_mask):
    ip = socket.inet_pton(socket.AF_INET6, ip).hex()
    ip_bin = bin(int(ip, 16)).replace('0b', '')
    truncated_ip = ip_bin[:int(subnet_mask)]
    return truncated_ip


def main(param):
    if ' ' in param:
        print("parm not right, exit...")
        raise Exception("param not right")
    param = param.split("-")
    param_number = 8
    if len(param) == param_number:
        ips, netdetect_ips, gateways, netmask, roce_port, bitmap, dscp_tc, common_network = param
    else:
        print("parm size not right, exit...")
        raise Exception("param size not right")

    info = {}
    gateway_set = set()
    npu_ids = []
    is_910b = False
    err_code, npu_info = get_statusoutput('npu-smi info -m')
    is_910b_pattern = re.compile("Ascend 910B[1-4]")
    if err_code:
        raise Exception("npu-smi call failed!")
    for line in npu_info.split('\n'):
        if 'Ascend Ascend910' in line:
            npu_id = line.strip().split()[3]
            if not npu_id.isdigit():
                raise Exception("npu id not right, exiting...")
            npu_ids.append(int(npu_id))
        elif 'Ascend 910' in line:
            npu_id = line.strip().split()[0]
            if not npu_id.isdigit():
                raise Exception("npu id not right, exiting...")
            npu_ids.append(int(npu_id))
        if re.search(is_910b_pattern, line):
            is_910b = True
    if not npu_ids:
        raise Exception("No training device found!")
    working_on_ipv6 = is_ipv6(ips)
    for _id, (npu_id, ip, netdetect_ip) in enumerate(zip(npu_ids, ips.split(','), netdetect_ips.split(','))):
        if working_on_ipv6 != is_ipv6(ip) or working_on_ipv6 != is_ipv6(netdetect_ip):
            raise Exception("Mix IPv4 and IPv6 when setting hccn!")
        if not working_on_ipv6:
            matching_gateway, matching_network = get_gateway(ip, gateways, netmask)
        else:
            matching_gateway, matching_network = get_ipv6_gateway(ip, gateways, netmask)

        gateway_set.add(matching_gateway)
        info[npu_id] = {
            'id': _id, 'ip': ip, 'common_network': common_network, 'sub_network': matching_network,
            'netdetect': netdetect_ip, 'gateway': matching_gateway
        }
    common_info = {'netmask': netmask, 'roce_port': roce_port, 'dscp_tc': dscp_tc, 'bitmap': bitmap, 'is_910b': is_910b,
                   'ipv6': working_on_ipv6}
    content = get_content(common_info, info, len(gateway_set))
    mode = 0o644
    fid = os.open("/etc/hccn.conf", os.O_RDWR | os.O_CREAT | os.O_TRUNC, mode)
    try:
        os.write(fid, content.encode('utf-8'))
    finally:
        os.close(fid)

    code, out = get_statusoutput("hccn_tool -a -cfg recovery")
    print(out)
    if code != 0:
        print("recovery hccn failed!")
        raise Exception("calling for hccn_tool failed")


def get_ipv6_gateway(ip, gateways, netmask):
    for gateway in gateways.split(','):
        if is_same_ipv6_subnet(ip, gateway, netmask):
            matching_gateway = gateway
            matching_network = 'INVALID'  # ipv6 do not need subnet route
            return matching_gateway, matching_network
    raise Exception("IPv6 gateway not found!")


def get_content(common_info, info, gateway_count):
    content = ""
    macs = {}
    table_start = 100
    is_standard_card = False
    # 非模组形态
    err_code, npu_info = get_statusoutput("npu-smi info -t board -i %s" % list(info.keys())[0])
    if err_code:
        raise Exception("npu-smi call failed!")
    for line in npu_info.split('\n'):
        if "Board ID" not in line:
            continue
        lower_tmp_list = line.lower()
        tmp_line = lower_tmp_list.split(":")
        if len(tmp_line) >= 2 and tmp_line[1].strip() in ("0xc0", "0xdf", "0xe1"):
            is_standard_card = True
            break
    for dev_id in info.keys():
        err_code, mac = get_statusoutput('hccn_tool -i %s -mac -g' % dev_id)
        if not err_code:
            mac = mac.replace("mac addr: ", "").strip()
            macs[dev_id] = mac
    for dev_id in info.keys():
        table_id = table_start + int(dev_id)
        _info = info.get(dev_id, {})
        content += get_basic_defines(common_info, _info, dev_id)
        content += get_gateway_defines(common_info, _info, dev_id)
        if common_info.get('is_910b', False):
            continue
        # 非模组形态
        if is_standard_card:
            continue
        content += IP_RULE_TEMPLATE % (dev_id, _info.get('ip'), table_id)
        content += IP_ROUTE_TEMPLATE % (dev_id, _info.get("common_network"), _info.get("gateway"), dev_id, table_id)
        # 非全连接组网
        if gateway_count > 1:
            continue
        content += IP_ROUTE_TEMPLATE % (dev_id, _info.get("sub_network"), _info.get("ip"), dev_id, table_id)

        for other_dev_id in info.keys():
            if int(dev_id) < SECOND_GROUP[0]:
                group = FIRST_GROUP
            else:
                group = SECOND_GROUP
            if other_dev_id not in group or dev_id == other_dev_id:
                continue
            content += ARP_TEMPLATE % (dev_id, dev_id, info.get(other_dev_id, {}).get("ip"),
                                       macs.get(other_dev_id))
    return content


def get_gateway_defines(common_info, _info, dev_id):
    content = ""
    if not _info.get('gateway'):
        raise Exception("gateway param not correct")
    if common_info.get('ipv6', False):
        template = IPV6_GATEWAY_TEMPLATE
    else:
        template = GATEWAY_TEMPLATE
    content += template % (dev_id, _info.get('gateway'))
    return content


def get_basic_defines(common_info, _info, dev_id):
    if common_info.get('ipv6', False):
        template = IPV6_ADDRESS_TEMPLATE
    else:
        template = ADDRESS_TEMPLATE
    content = template % (dev_id, _info.get("ip"), dev_id, common_info.get("netmask"),
                          dev_id, _info.get("netdetect"))
    if common_info.get("dscp_tc").strip():
        content += DSCP_TC_TEMPLATE % (dev_id, common_info.get('dscp_tc'))
    if common_info.get("bitmap").strip():
        content += BITMAP_TEMPLATE % (dev_id, common_info.get("bitmap"))
    return content


def ip_to_int(ip):
    oct_multiper = 8
    return sum(int(octet) << (oct_multiper * i) for i, octet in enumerate(reversed(ip.split('.'))))


def mask_to_cidr(mask):
    return sum(bin(int(octet)).count('1') for octet in mask.split('.'))


def is_ip_in_subnet(ip, gateway_ip, subnet_mask):
    ip_int = ip_to_int(ip)
    gateway_ip_int = ip_to_int(gateway_ip)
    subnet_mask_int = ip_to_int(subnet_mask)
    return (ip_int & subnet_mask_int) == (gateway_ip_int & subnet_mask_int)


def get_subnet(gateway_ip, subnet_mask):
    subnet_prefix_length = mask_to_cidr(subnet_mask)
    gateway_ip_octets = [int(octet) for octet in gateway_ip.split(".")]
    subnet_mask_octets = [int(octet) for octet in subnet_mask.split(".")]
    network_address_octets = [gateway_ip_octets[i] & subnet_mask_octets[i] for i in range(4)]
    network_address = ".".join([str(octet) for octet in network_address_octets])
    subnet = "{}/{}".format(network_address, subnet_prefix_length)
    return subnet


def get_gateway(_ip, gateways, netmask):
    for gateway in gateways.split(','):
        network = get_subnet(gateway, netmask)
        if is_ip_in_subnet(_ip, gateway, netmask):
            return gateway, network

    return "", ""


def get_statusoutput(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    stdout_str = stdout.decode('utf-8')
    stderr_str = stderr.decode('utf-8')
    return return_code, stdout_str + stderr_str


if __name__ == "__main__":
    ERR_EXISTING = False
    try:
        if len(sys.argv) != 2:
            raise Exception("param size not right")
        main(sys.argv[1])
    except Exception as e:
        print("error happen!")
        print(e)
        ERR_EXISTING = True
    if ERR_EXISTING:
        sys.exit(RET_ERROR_CODE)
