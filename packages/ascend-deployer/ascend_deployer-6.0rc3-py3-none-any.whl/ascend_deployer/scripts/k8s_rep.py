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
# ===========================================================================firmware_ver
import os.path
import subprocess
import json
import sys
import time
from collections import OrderedDict

require_by_all = ["calico-node", "kube-proxy", ]
master_by_scene = {'1': ["etcd", "kube-apiserver", "kube-controller-manager", "kube-scheduler"],
                   '2': ["etcd", "kube-apiserver", "kube-scheduler"],
                   '3': ["etcd", "kube-apiserver", "kube-scheduler"],
                   '4': ["etcd", "kube-apiserver", "kube-controller-manager", "kube-scheduler", "ascend-cert",
                         "ascend-edge", "ascend-ngnix"]
                   }

all_master_together_by_scene = {'1': ["calico-kube-controllers", "coredns", "hccl-controller", "ascend-operator",
                                      "clusterd", "volcano-scheduler", "volcano-controllers"],
                                '2': ["calico-kube-controllers", "coredns",
                                      "volcano-scheduler", "volcano-controllers", ],
                                '3': ["calico-kube-controllers", "coredns"],
                                '4': ["calico-kube-controllers", "coredns"]
                                }

worker_by_scene = {
    '1': ["ascend-device-plugin", "noded", "npu-exporter", ],
    '2': ["ascend-device-plugin", ],
    '3': ["ascend-device-plugin", ]
}


def get_nodes_info():
    result = subprocess.check_output(['kubectl', 'get', 'nodes', '-o', 'json'])
    nodes_info = json.loads(result)
    k8s_node = {}
    for node_json in nodes_info.get("items", {}):
        node = K8sNode(**node_json)
        ip_address = node.get_ip()
        property_dict = OrderedDict()
        property_dict['node name'] = node.get_name()
        property_dict['node type'] = node.get_type()
        property_dict['status'] = node.get_status()
        k8s_node[ip_address] = property_dict
    return k8s_node


def get_pods_info(nodes_dict):
    result = subprocess.check_output(['kubectl', 'get', 'pods', '-A', '-o', 'json'])
    pods_info = json.loads(result)
    for pod_json in pods_info.get("items", {}):
        pod = K8sPod(**pod_json)
        ip = pod.get_ip()
        property_dict = nodes_dict.get(ip, {})
        name = pod.get_name()
        if pod.get_status():
            property_dict.setdefault('ready pods', [])
            property_dict.get('ready pods', []).append(name)
        else:
            property_dict.setdefault('failed pods', [])
            property_dict.get('failed pods', []).append(name)

    return nodes_dict


def update_missing_pods(info, require_list):
    already_pods = info.get("ready pods", [])
    missing_pods = info.get("missing pods", [])
    for require_pod in require_list:
        flag = False
        for ready_pod in already_pods:
            if ready_pod.startswith(require_pod):
                flag = True
                break
        if not flag:
            missing_pods.append(require_pod)
            info["missing pods"] = missing_pods
    return info


def missing_add_to_all_master(temp_dict, node_dict):
    for _, info in node_dict.items():
        character = info.get("node type", "")
        if "master" in character:
            info.get("missing pods", []).extend(temp_dict.get("missing pods", []))


def check_missing_pods(node_dict, scene):
    all_master_pods = []
    for ip, info in node_dict.items():
        info = update_missing_pods(info, require_by_all)
        character = info.get("node type", "")
        if "master" in character:
            require_list = master_by_scene.get(scene, [])
            node_dict[ip] = update_missing_pods(info, require_list)
            all_master_pods.extend(info.get("ready pods", []))
        if "worker" in character:
            require_list = worker_by_scene.get(scene, [])
            node_dict[ip] = update_missing_pods(info, require_list)
    temp_dict = {"ready pods": all_master_pods}
    temp_dict = update_missing_pods(temp_dict, all_master_together_by_scene.get(scene, []))
    missing_add_to_all_master(temp_dict, node_dict)
    return node_dict


def is_dl_success(node_dict):
    for _, info in node_dict.items():
        if info.get("status", "") != "Ready":
            return False
        if len(info.get("missing pods", [])) > 0:
            return False
        if len(info.get("failed pods", [])) > 0:
            return False
    return True


def append_result(node_dict, result):
    for _, info in node_dict.items():
        info.setdefault("dl result", result)


def is_all_pods_ready():
    try:
        result = subprocess.check_output(['kubectl', 'get', 'pods', '-A', '-o', 'json'])
    except Exception as err:
        print(err)
        return False
    pods_info = json.loads(result)
    for pod_json in pods_info.get("items", {}):
        pod = K8sPod(**pod_json)
        if not pod.get_status():
            return False
    return True


class K8sPod:
    def __init__(self, status=None, metadata=None, **kwargs):
        self.status = PodStatus(**status)
        self.metadata = metadata

    def get_ip(self):
        return self.status.host_ip or ''

    def get_name(self):
        if isinstance(self.metadata, dict) and 'name' in self.metadata:
            return self.metadata.get('name', '')
        return ''

    def get_status(self):
        if self.status.container_statuses:
            return self.status.container_statuses[0].get('ready', False)
        return False


class PodStatus:
    def __init__(self, **kwargs):
        self.host_ip = kwargs.get('hostIP')
        self.container_statuses = kwargs.get('containerStatuses')


class K8sNode:
    def __init__(self, status=None, metadata=None, **kwargs):
        self.status = NodeStatus(**(status or {}))
        self.metadata = MetaData(**(metadata or {}))

    def get_ip(self):
        if self.status.addresses:
            return self.status.addresses[0].get('address', 'NA')
        return ''

    def get_name(self):
        if self.status.addresses:
            return self.status.addresses[1].get('address', 'NA')
        return ''

    def get_type(self):
        if self.metadata.labels.get("masterselector") and self.metadata.labels.get("workerselector"):
            return "master,worker"
        elif self.metadata.labels.get("masterselector"):
            return "master"
        elif self.metadata.labels.get("workerselector"):
            return "worker"
        else:
            return ''

    def get_status(self):
        if isinstance(self.status.conditions, list) and len(self.status.conditions) >= 2:
            return self.status.conditions[-1].get("type", "")
        return ''

    def get_npu(self):
        devices = []
        for key, value in self.status.capacity.items():
            if "huawei" in key:
                devices.append("%s:%s" % (key, value))
        return devices


class MetaData:
    def __init__(self, labels=None, **kwargs):
        self.labels = labels


class NodeStatus:
    def __init__(self, addresses=None, capacity=None, conditions=None, **kwargs):
        if not isinstance(addresses, list) or len(addresses) < 2:
            raise Exception('json format error, wrong address: %s' % str(addresses))
        self.addresses = addresses
        self.capacity = capacity
        self.conditions = conditions


def main(path_name, scene):
    path_name = os.path.realpath(os.path.expanduser(path_name))
    if os.path.exists(os.path.join(path_name, 'node_dict.json')):
        os.unlink(os.path.join(path_name, 'node_dict.json'))
    node_dict = get_nodes_info()

    try_times = 0
    while try_times < 5:
        if is_all_pods_ready():
            break
        try_times += 1
        time.sleep(2)

    node_dict = get_pods_info(node_dict)
    node_dict = check_missing_pods(node_dict, scene)
    if is_dl_success(node_dict):
        append_result(node_dict, "success")
    else:
        append_result(node_dict, "failed")
    if os.path.isdir(path_name):
        flags = os.O_WRONLY | os.O_CREAT
        with os.fdopen(os.open(os.path.join(path_name, 'node_dict.json'), flags, 0o700), 'w') as f:
            json.dump(node_dict, f)


if __name__ == '__main__':
    path = sys.argv[1]
    scene_num = sys.argv[2]
    try:
        main(path, scene_num)
    except Exception as e:
        print(e)
