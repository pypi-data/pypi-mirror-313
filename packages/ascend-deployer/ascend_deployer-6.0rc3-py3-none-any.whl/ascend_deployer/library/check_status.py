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
import os
import glob
import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_utils import clean_env, compare_version


class Check(object):
    max_k8s_version = '1.26'
    new_k8s_version = '1.20'
    mini_k8s_version = '1.19.16'

    def __init__(self):
        self.module = AnsibleModule(argument_spec=dict(
            tags=dict(type='list'),
            master_groups=dict(type='list'),
            worker_groups=dict(type='list'),
            current_hostname=dict(type='str'),
            use_k8s_version=dict(type='str')

        ))
        self.tags = self.module.params['tags']
        self.master_groups = self.module.params['master_groups']
        self.worker_groups = self.module.params['worker_groups']
        self.current_hostname = self.module.params['current_hostname']
        self.use_k8s_version = self.module.params['use_k8s_version']
        self.facts = dict()
        self.kubeadm_version = ''
        self.kubectl_version = ''
        self.kubelet_version = ''
        self.facts['use_old_k8s_version'] = old = compare_version(self.use_k8s_version, self.new_k8s_version) < 0
        self.facts.update({
            'import_cmd': 'docker load -i' if old else 'ctr -n=k8s.io images import'
        })

    def check_k8s_version(self):
        kubeadm_bin = self.module.get_bin_path('kubeadm')
        if kubeadm_bin:
            _, out, _ = self.module.run_command('kubeadm version', check_rc=True)
            reg = re.search(r'GitVersion:\"v(.+?)\"', out)
            if reg:
                self.kubeadm_version = reg.group(1)
        kubectl_bin = self.module.get_bin_path('kubectl')
        if kubectl_bin:
            _, out, _ = self.module.run_command('kubectl version')
            reg = re.search(r'GitVersion:\"v(.+?)\"', out)
            if reg:
                self.kubectl_version = reg.group(1)
        kubelet_bin = self.module.get_bin_path('kubelet')
        if kubelet_bin:
            _, out, _ = self.module.run_command('kubelet --version', check_rc=True)
            self.kubelet_version = re.search(r'(?<=v)\d+\.\d+(\.\d+)?', out).group()
        self.facts['k8s_installed'] = bool(self.kubeadm_version or self.kubectl_version or self.kubelet_version)
        if not all((self.kubeadm_version, self.kubectl_version, self.kubelet_version)):
            msg = 'Please install k8s first or confirm components of k8s, kubeadm_version: {}, kubectl_version: {}, '\
                  ' kubelet_version: {}'.format(self.kubeadm_version, self.kubectl_version, self.kubelet_version)
            self.module.fail_json(msg)
        if self.kubeadm_version != self.kubectl_version or self.kubeadm_version != self.kubelet_version:
            msg = 'k8s on this node has different version, kubeadm_version: {}, kubectl_version: {},' \
                  'kubelet_version: {}'.format(self.kubeadm_version, self.kubectl_version, self.kubelet_version)
            self.module.fail_json(msg)
        if compare_version(self.kubelet_version, self.max_k8s_version) >= 0:
            self.module.fail_json(msg='node k8s version should be < {}'.format(self.max_k8s_version))
        if compare_version(self.kubelet_version, self.mini_k8s_version) < 0:
            self.module.fail_json(msg='node k8s version should be >= {}'.format(self.mini_k8s_version))

    def check_driver_status(self):
        if self.current_hostname not in self.worker_groups:
            return
        if not self.module.get_bin_path('npu-smi'):
            self.module.fail_json(msg='please check that this node has the driver installed.')
        rc, out, err = self.module.run_command('lspci')
        if rc or err:
            self.module.fail_json(msg='can lspci failed: {}'.format(err))
        if not ('processing_accelerator' in out and 'Device d801' in out):
            return
        devices = glob.glob('/dev/davinci[0-9]*')
        if not devices:
            self.module.warn('no davinci device')
        if not self.module.get_bin_path('hccn_tool'):
            return
        for device in devices:
            device_id = device.replace('/dev/davinci', '')
            cmd = 'hccn_tool -i {} -ip -g'.format(device_id)
            rc, out, err = self.module.run_command(cmd)
            if rc or err:
                self.module.fail_json(msg='run cmd failed: {}'.format(err))
            if 'ipaddr' not in out:
                self.module.warn('{} has no device IP'.format(device_id))

    def run(self):
        clean_env()
        if self.current_hostname in self.master_groups + self.worker_groups:
            self.check_k8s_version()
        self.check_driver_status()
        self.module.exit_json(msg='check ok', ansible_facts=self.facts)


if __name__ == '__main__':
    Check().run()
