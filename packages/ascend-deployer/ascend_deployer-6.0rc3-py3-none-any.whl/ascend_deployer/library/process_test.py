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
import os.path
import subprocess

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import common_info
from ansible.module_utils.common_utils import generate_table

OK = "OK"
ERROR = "ERROR"

messages = []


def run_command(command, custom_env=None):
    try:
        env = os.environ.copy()
        if custom_env:
            env.update(custom_env)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env, executable="/bin/bash")
        stdout, stderr = process.communicate()
        if not isinstance(stdout, str):
            stdout = str(stdout, encoding='utf-8')
        if not isinstance(stderr, str):
            stderr = str(stderr, encoding='utf-8')
        return process.returncode == 0, stdout + stderr
    except Exception as e:
        return False, str(e)


def find_files(dir_path, file_name):
    targets = set()
    if not os.path.isdir(dir_path):
        return targets
    for root, _, files in os.walk(dir_path):
        if file_name in files:
            targets.add(os.path.realpath(os.path.join(root, file_name)))
    return targets


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


def get_npu_ids():
    ok, outputs = run_command("npu-smi info -m")
    if not ok:
        messages.append(outputs)
        return []
    npu_ids = []
    for line in outputs.splitlines():
        split_line = line.split()
        if not split_line:
            continue
        if '310' in split_line[-1] or '910' in split_line[-1] or '710' in split_line[-1]:
            npu_ids.append(split_line[0].strip())
    return npu_ids


def test_driver(cus_npu_info):
    if not os.path.exists("/usr/local/Ascend/driver/version.info"):
        return "not installed", ""
    ok, output = run_command(
        "npu-smi info",
        {"LD_LIBRARY_PATH": "/usr/local/Ascend/driver/lib64:/usr/local/Ascend/driver/lib64/common:"
                            "/usr/local/Ascend/driver/lib64/driver:"})
    if not ok:
        return ERROR, ""
    pattern = r"Version:\s*(\S+)"
    version = re.findall(pattern, output)[0].upper()

    if cus_npu_info == "300i-pro":
        checking_words = "300i"
    elif cus_npu_info == "300v-pro":
        checking_words = "300v"
    else:
        return OK, version

    for npu_id in get_npu_ids():
        ok, outputs = run_command("npu-smi info -t product -i {}".format(npu_id))
        if not ok:
            return ERROR, ""
        if checking_words not in outputs.lower():
            messages.append("you are installing driver of {} on hardware of {}".format(
                cus_npu_info, "300i-pro" if cus_npu_info == "300v-pro" else "300v-pro"))
            return ERROR, ""
    return OK, version


def test_firmware():
    if not os.path.exists("/usr/local/Ascend/firmware/version.info"):
        return "not installed", ""

    if not os.path.exists("/usr/local/Ascend/driver/tools/upgrade-tool"):
        return "not installed", ""
    ok, output = run_command(
        "/usr/local/Ascend/driver/tools/upgrade-tool --device_index -1 --system_version",
        {"LD_LIBRARY_PATH": "/usr/local/Ascend/driver/lib64:/usr/local/Ascend/driver/lib64/common:"
                            "/usr/local/Ascend/driver/lib64/driver:"})
    if ok and "succeed" in output:
        with open('/usr/local/Ascend/firmware/version.info', 'r') as file:
            content = file.read()
        pattern = r"Version=(\S+)"
        match = re.search(pattern, content)
        version = match.group(1) if match else ""
        return OK, version
    return ERROR, ""


def test_toolbox():
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    bin_path = os.path.join(ascend_install_path, "toolbox/latest/Ascend-DMI/bin/ascend-dmi")
    if not os.path.exists(bin_path):
        return "not installed", ""
    commands = [". {}/toolbox/set_env.sh".format(ascend_install_path), "ascend-dmi -v"]
    ok, output = run_command(" && ".join(commands))
    if ok:
        return OK, get_cann_version('toolbox')
    return ERROR, ""


def set_cann_env():
    """
    description: 设置环境变量，优先级： toolkit > nnae
    """
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    commands = []
    if os.path.exists("{}/ascend-toolkit/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/ascend-toolkit/set_env.sh".format(ascend_install_path))
    if os.path.exists("{}/nnae/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/nnae/set_env.sh".format(ascend_install_path))
    return commands


def test_python_package(package_name, python_version):
    local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    paths = os.environ.get("PATH", "")
    paths = "{}/{}/bin:".format(local_path, python_version) + paths
    ld_paths = "{}/{}/lib:".format(local_path, python_version)
    ok, output = run_command("python3 -m pip list | grep {} | grep -v torch-mindio".format(package_name), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return "not installed", ""
    paths = "{}/ascend-toolkit/latest/atc/ccec_compiler/bin/:".format(ascend_install_path) + paths
    ld_paths = ("{}/gcc7.3.0/lib64;{}/{}/lib/{}/site-packages/{}/lib:{}/add-ons/:".
                format(local_path, local_path, python_version, python_version[:9],
                       package_name, ascend_install_path) + ld_paths)
    commands = set_cann_env()
    if package_name == "torch":
        if not commands:
            return ERROR, ""
        commands.append('python3 -c "import torch; import torch_npu; a = torch.randn(3, 4).npu(); print(a + a)"')
    if package_name == "mindspore":
        commands.append('python3 -c "import mindspore;mindspore.set_context(device_target=\'Ascend\');\
        mindspore.run_check()"')
    ok, output = run_command(" && ".join(commands), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return ERROR, ""
    if package_name == "torch":
        package_name = "torch_npu"
    commands = set_cann_env()
    commands.append('python3 -c "import {}; print({}.__version__)"'.format(package_name, package_name))
    ok, output = run_command(" && ".join(commands), custom_env={"PATH": paths, "LD_LIBRARY_PATH": ld_paths})
    version = output.split('\n')[0]
    return OK, version


def test_tensorflow(python_version):
    local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    paths = os.environ.get("PATH", "")
    paths = "{}/{}/bin:".format(local_path, python_version) + paths
    ld_paths = "{}/{}/lib:{}/add-ons/:".format(local_path, python_version, ascend_install_path)
    ok, output = run_command('python3 -m pip list | grep -E "tensorflow |tensorflow-cpu"', custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return "not installed", ""
    if "1.15.0" in output:
        version = "1.15.0"
    elif "2.6.5" in output:
        version = "2.6.5"
    else:
        return ERROR, ""

    commands = [". {}/tfplugin/set_env.sh".format(ascend_install_path)]
    if os.path.exists("{}/nnae/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/nnae/set_env.sh".format(ascend_install_path))
    if os.path.exists("{}/ascend-toolkit/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/ascend-toolkit/set_env.sh".format(ascend_install_path))
    if version == "1.15.0":
        commands.append('python3 -c "import npu_bridge.estimator; import npu_bridge.hccl;'
                        ' from tensorflow.core.protobuf import rewriter_config_pb2"')
    if version == "2.6.5":
        commands.append('python3 -c "import npu_device; from tensorflow.core.protobuf import rewriter_config_pb2"')

    ok, output = run_command(" && ".join(commands), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    messages.append(output)
    if not ok:
        return ERROR, ""

    return OK, version

def test_tfplugin():
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    tfplugin_path = os.path.join(ascend_install_path, "tfplugin/latest")
    if not os.path.exists(tfplugin_path):
        return "not installed", ""
    return OK, get_cann_version('tfplugin')


def get_value_on_prefix_ignore_case(_dict, _key, default=None):
    for key, value in _dict.items():
        if key.lower().startswith(_key.lower()):
            return value
    return default


def get_cann_version(item):
    root_path = '/usr/local/Ascend'
    _item = item
    if item == 'ascend-toolkit':
        _item = 'toolkit'
    item_info_dir = os.path.join(root_path, item, "latest")
    target_paths = find_files(item_info_dir, "ascend_" + _item + "_install.info")
    version = ""
    for info_path in target_paths:
        item_info = info_to_dict(info_path)
        version = get_value_on_prefix_ignore_case(item_info, "version", "")
    return version


def test_cann_packages(package_name, python_version):
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    cann_path = os.path.join(ascend_install_path, "{}/latest".format(package_name))
    if not os.path.exists(cann_path):
        return "not installed", ""
    commands = []
    if os.path.exists("{}/{}/set_env.sh".format(ascend_install_path, package_name)):
        commands.append(". {}/{}/set_env.sh".format(ascend_install_path, package_name))
    else:
        return ERROR, ""
    commands.append('python3 -c "import acl"')
    paths = os.environ.get("PATH", "")
    local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
    paths = "{}/{}/bin:".format(local_path, python_version) + paths
    ld_paths = "{}/{}/lib:".format(local_path, python_version)
    ok, output = run_command(" && ".join(commands), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return ERROR, ""
    return OK, get_cann_version(package_name)


def test_fault_diag():
    try:
        env = os.environ.copy()
        process = subprocess.Popen("ascend-fd version", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env, executable="/bin/bash")
        stdout, stderr = process.communicate()
        if not isinstance(stdout, str):
            stdout = str(stdout, encoding='utf-8')
        if not isinstance(stderr, str):
            stderr = str(stderr, encoding='utf-8')
        if process.returncode == 0:
            pattern = r"ascend-fd v(\d+\.\d+\.\w+)"
            match = re.search(pattern, stdout + stderr)
            version = match.group(1) if match else ""
            return OK, version
        elif process.returncode == 127:
            return "not installed", ""
    except Exception:
        return ERROR, ""
    return ERROR, ""


def main():
    module = AnsibleModule(argument_spec=dict(
            ansible_run_tags=dict(type="list", required=True),
            cus_npu_info=dict(type="str", required=True),
            ip=dict(type="str", required=True),
            python_version=dict(type="str", required=True)
        )
    )
    ansible_run_tags = set(module.params["ansible_run_tags"])
    cus_npu_info = module.params.get("cus_npu_info", "")
    python_version = module.params.get("python_version", "")
    if 'whole' in ansible_run_tags:
        ansible_run_tags = ["driver", "firmware", "toolbox", "mindspore",
                            "pytorch", "tensorflow", "tfplugin", "nnae",
                            "nnrt", "toolkit", "fault-diag"]
    result = {}
    if "driver" in ansible_run_tags:
        result["driver"] = test_driver(cus_npu_info)
    if "firmware" in ansible_run_tags:
        result["firmware"] = test_firmware()
    if "toolbox" in ansible_run_tags:
        result["toolbox"] = test_toolbox()
    if "mindspore" in ansible_run_tags:
        result["mindspore"] = test_python_package("mindspore", python_version)
    if "pytorch" in ansible_run_tags:
        result["pytorch"] = test_python_package("torch", python_version)
    if "tensorflow" in ansible_run_tags:
        result["tensorflow"] = test_tensorflow(python_version)
    if "tfplugin" in ansible_run_tags:
        result["tfplugin"] = test_tfplugin()
    if "nnae" in ansible_run_tags:
        result["nnae"] = test_cann_packages("nnae", python_version)
    if "nnrt" in ansible_run_tags:
        result["nnrt"] = test_cann_packages("nnrt", python_version)
    if "toolkit" in ansible_run_tags:
        result["toolkit"] = test_cann_packages("ascend-toolkit", python_version)
    if "fault-diag" in ansible_run_tags:
        result["fault-diag"] = test_fault_diag()

    formatted_result = {module.params.get("ip", ""): result}

    module.exit_json(changed=True, rc=0, msg="\n".join(messages), result=formatted_result)


if __name__ == "__main__":
    main()
