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
import os
import grp
import pwd
import platform
import re
import shutil
import zipfile

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_utils import clean_env

name_list = [
    'device-plugin',
    'ascend-operator',
    'hccl-controller',
    'noded',
    'npu-exporter',
    'resilience-controller',
    'volcano',
    'clusterd'
]


class Installer(object):
    component_name = ''
    user = 'hwMindX'
    user_id = 9000
    group = 'hwMindX'
    group_id = 9000
    namespace = 'mindx-dl'

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                resources_dir=dict(type='str', required=True),
                step=dict(type='str', required=True),
                # if step == 'apply', below params are used
                node_name=dict(type='str'),
                master_node=dict(type='bool'),
                worker_node=dict(type='bool'),
                node_info=dict(type='dict')
            )
        )
        self.resources_dir = os.path.expanduser(self.module.params['resources_dir'])
        self.step = self.module.params['step']
        self.node_name = self.module.params['node_name']
        self.master_node = self.module.params['master_node']
        self.worker_node = self.module.params['worker_node']
        self.node_info = self.module.params['node_info']
        self.arch = platform.machine()
        self.dl_dir = os.path.join(self.resources_dir, 'mindxdl')
        self.base_images_dir = os.path.join(self.dl_dir, 'baseImages', self.arch)
        self.package_dir = os.path.join(self.dl_dir, 'dlPackage', self.arch)
        self.extract_dir = os.path.join(self.dl_dir, 'dlDeployPackages', self.arch, self.component_name)
        self.images_dir = os.path.join(self.dl_dir, 'dlImages', self.arch, self.component_name)
        self.yaml_dir = os.path.join(self.dl_dir, 'yamls', self.arch)
        self.dl_log = '/var/log/mindx-dl'
        self.use_new_k8s = True
        self.import_cmd = ''
        self.yaml_file_path = ''
        self.images = dict()
        self.facts = dict()

    def is_new_k8s_version(self):
        if not self.module.get_bin_path('kubelet'):
            self.module.fail_json(msg='failed to find kubelet, is k8s installed correctly?')
        rc, out, err = self.module.run_command('kubelet --version')
        if rc or 'Kubernetes' not in out:
            self.module.fail_json(msg='failed to get kubelet version, out:{}, err:{}'.format(out, err))
        version = re.search(r'(?<=v)\d+\.\d+(\.\d+)?', out).group()
        version_tuple = tuple(map(int, version.split('.')))
        return version_tuple > (1, 19, 16)

    def get_yaml_path(self):
        """ pick the right yaml file and return file path """
        for root, _, files in os.walk(self.extract_dir):
            for filename in files:
                if filename.endswith('.yaml') and 'without' not in filename and '1usoc' not in filename:
                    return os.path.join(root, filename)
        self.module.fail_json('failed to find yaml in {}'.format(self.extract_dir))
        return ""

    def check_and_prepare(self):
        if self.component_name not in name_list:
            self.module.fail_json(msg='invalid component name, choice from {}'.format(name_list))
        clean_env()
        self.use_new_k8s = self.is_new_k8s_version()
        src = ''
        for pkg in os.listdir(self.package_dir):
            if self.component_name in pkg:
                src = os.path.join(self.package_dir, pkg)
                break
        if not src:
            self.module.fail_json(msg='failed to find {} in path: {}'.format(self.component_name, self.package_dir))
        if os.path.exists(self.extract_dir):
            shutil.rmtree(self.extract_dir)
        with zipfile.ZipFile(src) as zf:
            zf.extractall(self.extract_dir)
        yaml_file = self.get_yaml_path()
        if not os.path.exists(yaml_file):
            self.module.fail_json(msg='failed to find yaml file: {}'.format(yaml_file))
        self.yaml_file_path = yaml_file
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir, 0o755)

    def get_image_tags(self):
        keyword = 'image:'
        image_tags = []
        with open(self.yaml_file_path) as f:
            for line in f:
                if keyword in line and line.strip() != keyword:
                    # like"      - image: ascend-k8sdeviceplugin:v5.0.0"
                    image_tag = line.replace(keyword, '').replace(' - ', '').strip()
                    if ':' in image_tag:
                        image_tags.append(image_tag)
        if not image_tags:
            self.module.fail_json(msg='failed to find image name in file: {}'.format(self.yaml_file_path))
        return image_tags

    def is_images_exist(self):
        for image_tag in self.get_image_tags():
            image_name, image_version = image_tag.split(':')
            image_name = image_name.split('/')[-1]
            image_save_name = '{}_{}.tar'.format(image_name, self.arch)
            self.images[image_tag] = image_save_name
        image_path_list = []
        exist = True
        for save_name in self.images.values():
            image_path = os.path.join(self.images_dir, save_name)
            image_path_list.append(image_path)
            if not os.path.exists(image_path):
                exist = False
        self.facts['{}_images'.format(self.component_name.replace('-', "_"))] = ' '.join(image_path_list)
        return exist

    def load_base_images(self):
        for image in os.listdir(self.base_images_dir):
            cmd = 'docker load -i {}'.format(image)
            self.module.run_command(cmd, cwd=self.base_images_dir, check_rc=True)
            self.module.log(msg='load image file: {} in {} successfully'.format(image, self.base_images_dir))

    def build_images(self):
        build_dir = os.path.dirname(self.yaml_file_path)
        for tag, save_name in self.images.items():
            self.module.run_command('docker build -t {} .'.format(tag), cwd=build_dir, check_rc=True)
            self.module.run_command('docker save -o {} {}'.format(save_name, tag), cwd=self.images_dir, check_rc=True)
            self.module.log(msg='build image file: {} in {} successfully'.format(save_name, self.images_dir))

    def build(self):
        if self.is_images_exist():
            self.module.exit_json(changed=False, msg='image exists, skip to build again', ansible_facts=self.facts)
        self.load_base_images()
        self.build_images()

    def iter_cmd_output(self, cmd):
        if not self.module.get_bin_path(cmd.split()[0]):
            return
        rc, out, err = self.module.run_command(cmd)
        if out:
            for line in out.splitlines():
                yield line

    @staticmethod
    def get_labels():
        """ return label list for specified component, override this method if needed """
        return []

    def collect_labels(self):
        master_labels = ['masterselector=dls-master-node']
        worker_labels = [
            'node-role.kubernetes.io/worker=worker',
            'workerselector=dls-worker-node',
        ]
        worker_labels.extend(self.get_labels())
        self.module.log(msg='worker labels {}'.format(str(worker_labels)))
        self.facts['{}_labels'.format(self.component_name.replace('-', "_"))] = {
            self.node_name: {
                'master_labels': master_labels,
                'worker_labels': worker_labels,
                'master_node': self.master_node,
                'worker_node': self.worker_node
            }
        }

    def load_images(self):
        image_dir = os.path.join(self.resources_dir, 'mindxdl', 'dlImages', self.arch, self.component_name)
        self.import_cmd = 'docker load -i' if not self.use_new_k8s else 'ctr -n=k8s.io images import'
        suffix = '' if not self.use_new_k8s else '--all-platforms'
        for image_file in os.listdir(image_dir):
            self.module.run_command('{} {} {}'.format(self.import_cmd, image_file, suffix),
                                    cwd=image_dir, check_rc=True)
            self.module.log(msg='load image file: {} in {} successfully'.format(image_file, image_dir))

    def ensure_group_exist(self):
        try:
            info = grp.getgrnam(self.group)
        except KeyError:
            info = None
        if not info:
            cmd = 'groupadd -g {} {}'.format(self.group_id, self.group)
            self.module.run_command(cmd, check_rc=True)
            return
        if info.gr_gid == self.group_id:
            return
        cmd = 'groupmod -g {} {}'.format(self.group_id, self.group)
        self.module.run_command(cmd, check_rc=True)

    def ensure_user_exist(self):
        try:
            info = pwd.getpwnam(self.user)
        except KeyError:
            info = None
        if not info:
            cmd = 'useradd -u {} -g {} -G {} -c {} -s {} -m {}'.format(
                self.user_id, self.group, self.group, self.user, self.module.get_bin_path('nologin'), self.user
            )
            self.module.run_command(cmd, check_rc=True)
            return
        if info.pw_uid == self.user_id:
            return
        cmd = 'usermod -u {} {}'.format(self.user_id, self.user)
        self.module.run_command(cmd, check_rc=True)

    def create_log_dir(self):
        """ do jobs such as creating log dir and logrotate file """
        log_dir_names = (self.component_name,)
        for log_dir in log_dir_names:
            log_path = os.path.join(self.dl_log, log_dir)
            if not os.path.exists(log_path):
                os.makedirs(log_path, 0o750)
                os.chown(log_path, self.user_id, self.group_id)

    def install(self):
        self.collect_labels()
        if not os.path.exists(self.dl_log):
            os.makedirs(self.dl_log, 0o755)
        self.load_images()
        self.ensure_group_exist()
        self.ensure_user_exist()
        self.create_log_dir()

    def _get_yaml_contents(self):
        with open(self.yaml_file_path) as f:
            return f.readlines()

    def create_namespace(self):
        cmd = 'kubectl create namespace {}'.format(self.namespace)
        self.module.run_command(cmd)
        self.module.log(msg='create namespace: {} for component: {}'.format(self.namespace, self.component_name))

    def clear_previous_pod(self, yaml_path):
        cmd = 'kubectl delete -f {}'.format(yaml_path)
        self.module.run_command(cmd)

    def label(self):
        all_cmd = ""
        for node_name in self.node_info.keys():
            labels = ""
            if self.node_info.get(node_name, {}).get('master_node'):
                master_labels = ' '.join(self.node_info.get(node_name, {}).get('master_labels', []))
                labels = labels + ' ' + master_labels
            if self.node_info.get(node_name, {}).get('worker_node'):
                worker_labels = ' '.join(self.node_info.get(node_name, {}).get('worker_labels', []))
                labels = labels + ' ' + worker_labels
            cmd = 'kubectl label --overwrite node {} {} & '.format(node_name, labels.strip())
            all_cmd += cmd
        all_cmd = all_cmd.strip(' & ')
        self.module.run_command(all_cmd, check_rc=True, use_unsafe_shell=True)
        self.module.log('run cmd: {} successfully'.format(all_cmd))

    def apply_yaml(self):
        if not os.path.exists(self.yaml_dir):
            os.makedirs(self.yaml_dir, 0o755)
        basename = os.path.basename(self.yaml_file_path)
        yaml_path = os.path.join(self.yaml_dir, basename)
        with open(yaml_path, 'w') as f:
            f.writelines(self._get_yaml_contents())
        self.clear_previous_pod(yaml_path)
        cmd = 'kubectl apply -f {}'.format(yaml_path)
        self.module.run_command(cmd, check_rc=True)
        self.module.log(msg='apply yaml: {} for component: {}'.format(yaml_path, self.component_name))

    def apply(self):
        self.create_namespace()
        self.label()
        self.apply_yaml()

    def run(self):
        steps = {
            'build': self.build,
            'install': self.install,
            'apply': self.apply
        }
        if self.step not in steps:
            self.module.fail_json(msg='invalid step: {}, choose from {}'.format(self.step, list(steps)))
        self.check_and_prepare()
        steps.get(self.step)()
        self.module.exit_json(
            changed=True,
            msg='{} component: {} successfully'.format(self.step, self.component_name),
            ansible_facts=self.facts)


