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
import re
import csv
import os.path
import subprocess

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_utils import generate_table

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


def get_dl_cluster_version(namespace, pod_name, cluster_name):
    """
    description: 通过进入组件pod中 执行可执行文件的--version命令，获得组件的版本号
    """
    command = 'kubectl exec -it -n {} {} -- {} --version'.format(namespace, pod_name, cluster_name)
    ok, output = run_command(command)
    pattern = r"version:\s*(v[\d\.A-Za-z]+)"
    match = re.search(pattern, output)
    if match:
        return match.group(1)
    else:
        return ""


def get_dl_k8s_pods(host_name=None):
    """
    description: 解析kubectl get pods -A回显信息(或仅查看当前node)，将NAME中有dl组件的pod结果存入dict并返回
    """
    if not host_name:
        ok, output = run_command("kubectl get pods -A")
    else:
        ok, output = run_command("kubectl get pods -A --field-selector spec.nodeName={}".format(host_name))
    if not ok:
        return {}
    dl_pods_info = {}

    # dl中的组件
    match_list = ['device-plugin', 'volcano', 'noded', 'clusterd',
                  'hccl-controller', 'ascend-operator', 'npu-exporter', 'resilience-controller']
    # 解析回显信息
    lines = output.split('\n')
    reader = csv.DictReader(lines, delimiter=' ', skipinitialspace=True)
    for row in reader:
        name = row['NAME']
        for match in match_list:
            if match in name:
                if match not in dl_pods_info:
                    dl_pods_info[match] = []
                dl_pods_info[match].append(row)
    return dl_pods_info


def get_k8s_nodes():
    """
    description: 解析kubectl get nodes回显信息，将node_name作为key存入dict并返回
    """
    ok, output = run_command("kubectl get nodes")
    if not ok:
        return {}
    nodes_info = {}

    # 解析回显信息
    lines = output.split('\n')
    reader = csv.DictReader(lines, delimiter=' ', skipinitialspace=True)
    for row in reader:
        node_name = row['NAME']
        if node_name:
            nodes_info[node_name] = row
    return nodes_info


def get_docker_images():
    """
    description: 解析docker images命令的回显信息，将REPOSITORY作为key存入dict并返回
    """
    ok, output = run_command("docker images --format 'table {{.Repository}} "
                             "{{.Tag}} {{.ID}} {{.CreatedSince}} {{.Size}}'")
    if not ok:
        return {}
    images_info = {}

    # 解析回显信息
    lines = output.split('\n')
    reader = csv.DictReader(lines, delimiter=' ', skipinitialspace=True)
    for row in reader:
        repository = row['REPOSITORY']
        if repository:
            images_info[repository] = row
    return images_info


def check_pods_status(pod_info):
    if pod_info.get('READY') == '1/1' and pod_info.get('STATUS') == 'Running':
        return OK
    return ERROR


def test_volcano(k8s_pods_info, all_k8s_pods_info):
    """
    description: 查看Ascend Volcano组件状态，仅有master节点会安装Volcano，
    每个master应有volcano-controllers和volcano-scheduler两个组件
    """
    def get_volcano_version(namespace, pod_name, cluster_name):
        command = 'kubectl exec -it -n {} {} -- {} --version'.format(namespace, pod_name, cluster_name)
        ok, output = run_command(command)
        output_dict = {}
        for line in output.strip().split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                output_dict[key.strip()] = value.strip()
        return output_dict.get('Version', '')
    volcano_controllers = {}
    volcano_scheduler = {}
    vc_controller_version = vc_scheduler_version = ""
    cnt = 0
    for pod in all_k8s_pods_info.get('volcano', []):
        # 验证命名空间
        if pod.get('NAMESPACE') == 'volcano-system':
            if 'volcano-controllers' in pod.get('NAME'):
                volcano_controllers = pod
                vc_controller_version = get_volcano_version('volcano-system',
                                                            pod.get('NAME'), '/vc-controller-manager')
            elif 'volcano-scheduler' in pod.get('NAME'):
                volcano_scheduler = pod
                vc_scheduler_version = get_volcano_version('volcano-system',
                                                           pod.get('NAME'), '/vc-scheduler')
    if not volcano_controllers and not volcano_scheduler:
        return 'not installed', ''
    result = "OK" if (check_pods_status(volcano_controllers) == "OK"
                      and check_pods_status(volcano_scheduler) == "OK") else "ERROR"
    version = vc_controller_version if vc_controller_version and vc_scheduler_version \
        else vc_controller_version or vc_scheduler_version or ""
    for pod in k8s_pods_info.get('volcano', []):
        if 'volcano-controllers' in pod.get('NAME') or 'volcano-scheduler' in pod.get('NAME'):
            cnt += 1
    if result == "OK" and not cnt:
        return '', ''
    return result, version


def test_dl_worker_cluster(k8s_pods_info, cluster_name, name_space):
    """
    description: 查看dl中worker节点下应仅有一个pod的组件状态
    """
    cluster = {}
    for pod in k8s_pods_info.get(cluster_name, []):
        # 验证命名空间
        if pod.get('NAMESPACE') == name_space:
            cluster = pod
    if not cluster:
        return 'not installed', ''
    version = get_dl_cluster_version(cluster.get('NAMESPACE'),
                                     cluster.get('NAME'), cluster_name)
    return check_pods_status(cluster), version


def test_clusterd(k8s_pods_info, all_k8s_pods_info):
    """
    description: 查看clusterd组件状态, rc2版本该组件应有3个pod，rc3版本该组件应有1个pod
    """
    clusterd_pods_cnt_dict = {
        'v6.0.RC2': 3,
        'v6.0.RC3': 1
    }
    node_cluster = {}
    pods_cnt = 0
    # 查看当前节点是否有对应组件
    for pod in k8s_pods_info.get("clusterd", []):
        # 验证命名空间
        if pod.get('NAMESPACE') == "mindx-dl":
            node_cluster = pod
    # 查看全部节点组件数量
    for pod in all_k8s_pods_info.get("clusterd", []):
        if pod.get('NAMESPACE') == "mindx-dl":
            pods_cnt += 1
    if not node_cluster and not pods_cnt:
        return 'not installed', ''

    # 查看clusterd版本
    version = get_dl_cluster_version(node_cluster.get('NAMESPACE'), node_cluster.get('NAME'), "clusterd")

    # 当前节点没有此组件，但是全部节点数量正常
    if not node_cluster and pods_cnt == clusterd_pods_cnt_dict.get(version):
        return '', ''
    # 当前节点有此组件，而且全部节点数量正常
    elif node_cluster and pods_cnt == clusterd_pods_cnt_dict.get(version):
        return check_pods_status(node_cluster), version
    else:
        return ERROR, ''


def test_dl_master_cluster(k8s_pods_info, all_k8s_pods_info, cluster_name, name_space):
    """
    description: 查看dl中master节点下应仅有一个pod的组件状态
    """
    cluster_pods_cnt_dict = {
        'ascend-operator': 1,
        'hccl-controller': 1
    }
    node_cluster = {}
    pods_cnt = 0
    # 查看当前节点是否有对应组件
    for pod in k8s_pods_info.get(cluster_name, []):
        # 验证命名空间
        if pod.get('NAMESPACE') == name_space:
            node_cluster = pod
    # 查看全部节点组件数量
    for pod in all_k8s_pods_info.get(cluster_name, []):
        if pod.get('NAMESPACE') == name_space:
            pods_cnt += 1
    if not node_cluster and not pods_cnt:
        return 'not installed', ''
    # 当前节点没有此组件，但是全部节点数量正常
    elif not node_cluster and pods_cnt == cluster_pods_cnt_dict.get(cluster_name):
        return '', ''
    # 当前节点有此组件，而且全部节点数量正常
    elif node_cluster and pods_cnt == cluster_pods_cnt_dict.get(cluster_name):
        version = get_dl_cluster_version(node_cluster.get('NAMESPACE'),
                                         node_cluster.get('NAME'), cluster_name)
        return check_pods_status(node_cluster), version
    else:
        return ERROR, ''


def test_resilience_controller(k8s_pods_info, all_k8s_pods_info):
    """
    description: 查看Ascend Resilience Controller组件状态，每个master节点应只有一个对应的pod
    """
    resilience_controller = {}
    cnt = 0
    for pod in k8s_pods_info.get('resilience-controller', []):
        # 验证命名空间
        if pod.get('NAMESPACE') == 'mindx-dl':
            resilience_controller = pod
    for pod in all_k8s_pods_info.get('resilience-controller', []):
        # 验证命名空间
        if pod.get('NAMESPACE') == 'mindx-dl':
            cnt += 1
    if not resilience_controller and not cnt:
        return 'not installed', ''
    elif not resilience_controller and cnt == 1:
        return '', ''
    elif resilience_controller and cnt == 1:
        # Ascend Resilience Controller 容器中没有可执行文件，使用docker imagers获取版本号
        version = get_dl_cluster_version(resilience_controller.get('NAMESPACE'), resilience_controller.get('NAME'),
                                         '/home/hwMindX/resilience-controller')
        return check_pods_status(resilience_controller), version
    else:
        return ERROR, ''


def list_to_dict(result_list):
    result_dict = {}
    for item in result_list:
        for key, value in item.items():
            if key not in result_dict:
                result_dict[key] = value
            else:
                result_dict[key].update(value)
    return result_dict


def main():
    """
    description: 安装在管理节点的组件：Ascend Operator、ClusterD、Resilience Controller、HCCL Controller、Volcano
                 安装在计算节点的组件：Ascend Device Plugin、Ascend Docker Runtime、NodeD、NPU Exporter
                 roles表示管理节点或者计算节点
    """
    module = AnsibleModule(argument_spec=dict(
            ansible_run_tags=dict(type="list", required=True),
            ip=dict(type="str", required=True),
            roles=dict(type="list", required=True),
            node_name=dict(type="str", required=True),
            cann_test_result=dict(type="list", required=True),
            docker_runtime_result=dict(type="list", required=True)
        )
    )

    docker_runtime_result = list_to_dict(module.params["docker_runtime_result"])

    ansible_run_tags = set(module.params["ansible_run_tags"])
    if 'whole' in ansible_run_tags:
        ansible_run_tags = ['ascend-device-plugin', 'volcano', 'noded', 'clusterd',
                            'hccl-controller', 'ascend-operator', 'npu-exporter', 'resilience-controller']

    result = {}
    nodes_info = get_k8s_nodes()
    all_k8s_pods_info = get_dl_k8s_pods()
    # 将docker runtime结果从list转换成dict
    for host_name, node_value in nodes_info.items():
        if not host_name:
            ok, output = run_command('hostname')
            if ok:
                host_name = output.strip()
            else:
                host_name = ' '
        k8s_pods_info = get_dl_k8s_pods(host_name)
        node = {}

        # 检查master节点的组件
        if 'control-plane' in node_value.get('ROLES') or 'master' in node_value.get('ROLES'):
            if "ascend-operator" in ansible_run_tags:
                node["ascend-operator"] = list(test_dl_master_cluster(k8s_pods_info, all_k8s_pods_info,
                                                            "ascend-operator", "mindx-dl"))
            if "clusterd" in ansible_run_tags:
                node["clusterd"] = list(test_clusterd(k8s_pods_info, all_k8s_pods_info))
            if "resilience-controller" in ansible_run_tags:
                node["resilience-controller"] = list(test_resilience_controller(k8s_pods_info, all_k8s_pods_info))
            if "hccl-controller" in ansible_run_tags:
                node["hccl-controller"] = list(test_dl_master_cluster(k8s_pods_info, all_k8s_pods_info,
                                                            "hccl-controller", "mindx-dl"))
            if "volcano" in ansible_run_tags:
                node["volcano"] = list(test_volcano(k8s_pods_info, all_k8s_pods_info))

        # 检查worker节点的组件
        if 'worker' in node_value.get('ROLES'):
            if "ascend-device-plugin" in ansible_run_tags:
                node["ascend-device-plugin"] = list(test_dl_worker_cluster(k8s_pods_info, "device-plugin",
                                                                 "kube-system"))
            if "noded" in ansible_run_tags:
                node["noded"] = list(test_dl_worker_cluster(k8s_pods_info, "noded", "mindx-dl"))
            if "npu-exporter" in ansible_run_tags:
                node["npu-exporter"] = list(test_dl_worker_cluster(k8s_pods_info,
                                                        "npu-exporter", "npu-exporter"))
        if host_name in result:
            result[host_name].update(node)
        else:
            result[host_name] = node

    # 合并worker中docker runtime和master中其他组件的结果
    for key, value in docker_runtime_result.items():
        if key in result:
            result[key].update(value)
        else:
            result[key] = value

    # 定义表格的列名
    columns_npu = ["driver", "firmware"]
    columns_cann = ["toolbox", "tfplugin", "nnae", "nnrt", "toolkit"]
    columns_pypkg = ["mindspore", "tensorflow", "pytorch", "fault-diag"]

    cann_result = list_to_dict(module.params["cann_test_result"])

    # 生成表
    table_npu = generate_table(cann_result, "npu-clusters", columns_npu, "npu")
    table_cann = generate_table(cann_result, "cann-clusters", columns_cann, "cann")
    table_pypkg = generate_table(cann_result, "pypkg-clusters", columns_pypkg, "pypkg")

    cann_table_result_str = "{}\n\n{}\n\n{}\n".format(table_npu, table_cann, table_pypkg)

    # 定义关于dl组件的两个表格的列名
    columns_master = ["ascend-operator", "clusterd", "hccl-controller", "volcano", "resilience-controller"]
    columns_worker = ["ascend-device-plugin", "ascend-docker-runtime", "noded", "npu-exporter"]

    # 生成管理节点表和计算节点表
    table_master = generate_table(result, "dl-clusters(master-node)", columns_master, "master-node")
    table_worker = generate_table(result, "dl-clusters(worker-node)", columns_worker, "worker-node")

    cann_test_result_str = dl_test_result = ""
    for node in module.params["cann_test_result"]:
        cann_test_result_str += '\n{}'.format(node)
    for node in result:
        dl_test_result += '\n{}: {}'.format(node, result.get(node))

    table_result_str = "[ASCEND]{}\n{}\n\n\n{}\n\n{}\n\n{}\n".format(cann_test_result_str, dl_test_result,
                                                                     cann_table_result_str, table_master,
                                                                     table_worker)

    return module.exit_json(changed=True, rc=0, msg=table_result_str)

if __name__ == "__main__":
    main()