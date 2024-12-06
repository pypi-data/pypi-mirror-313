#!/usr/bin/env python3
# coding: utf-8
# Copyright 2024 Huawei Technologies Co., Ltd
import os
import glob

tags_map = {
    'driver': {
        'need_nexus': False,
        'name_keywords': ['driver', 'npu'],
        'path_keywords': ['run_from_*_zip']
    },
    'firmware': {
        'need_nexus': False,
        'name_keywords': ['firmware', 'npu'],
        'path_keywords': ['run_from_*_zip']
    },
    'npu': {
        'need_nexus': False,
        'name_keywords': ['driver', 'firmware', 'npu'],
        'path_keywords': ['run_from_*_zip']
    },
    'atlasedge': {
        'need_nexus': False,
        'name_keywords': ['atlasedge', ],
        'path_keywords': ['run_from_*_zip']
    },
    'ha': {
        'need_nexus': False,
        'name_keywords': ['ha', ],
        'path_keywords': ['run_from_*_zip']
    },
    'ief': {
        'need_nexus': False,
        'name_keywords': ['ief', ],
        'path_keywords': ['run_from_*_zip']
    },
    'kernels': {
        'need_nexus': False,
        'name_keywords': ['kernels', ],
        'path_keywords': ['run_from_*_zip']
    },
    'nnae': {
        'need_nexus': False,
        'name_keywords': ['nnae', ],
        'path_keywords': ['run_from_*_zip']
    },
    'nnrt': {
        'need_nexus': False,
        'name_keywords': ['nnrt', ],
        'path_keywords': ['run_from_*_zip']
    },
    'tfplugin': {
        'need_nexus': False,
        'name_keywords': ['tfplugin', ],
        'path_keywords': ['run_from_*_zip']
    },
    'toolbox': {
        'need_nexus': False,
        'name_keywords': ['toolbox', ],
        'path_keywords': ['run_from_*_zip']
    },
    'toolkit': {
        'need_nexus': False,
        'name_keywords': ['toolkit', ],
        'path_keywords': ['run_from_*_zip', 'sources/*mpi*']
    },
    'auto': {
        'need_nexus': True,
        'name_keywords': ['npu', 'toolkit', 'nnrt', 'nnae', 'tfplugin', 'kernels', 'toolbox', 'faultdiag'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip', 'FaultDiag'],
    },
    'dl': {
        'need_nexus': False,
        'name_keywords': ['npu', ],
        'path_keywords': ['sources', 'run_from_*_zip', 'mindxdl/dlPackage', 'mindxdl/baseImages']
    },
    'edge': {
        'need_nexus': True,
        'name_keywords': ['atlasedge', 'ha'],
        'path_keywords': ['run_from_*_zip']
    },
    'mindspore': {
        'need_nexus': True,
        'name_keywords': ['npu', 'toolkit', 'kernels'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip']
    },
    'offline_dev': {
        'need_nexus': True,
        'name_keywords': ['npu', 'toolkit', 'kernels'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip']
    },
    'offline_run': {
        'need_nexus': True,
        'name_keywords': ['npu', 'nnrt'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip']
    },
    'pytorch_dev': {
        'need_nexus': True,
        'name_keywords': ['npu', 'toolkit', 'kernels'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip']
    },
    'pytorch_run': {
        'need_nexus': True,
        'name_keywords': ['npu', 'nnae', 'kernels'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip']
    },
    'tensorflow_dev': {
        'need_nexus': True,
        'name_keywords': ['npu', 'toolkit', 'kernels', 'tfplugin'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip']
    },
    'tensorflow_run': {
        'need_nexus': True,
        'name_keywords': ['npu', 'nnae', 'kernels', 'tfplugin'],
        'path_keywords': ['sources', 'pylibs', 'run_from_*_zip']
    },
    'mindstudio': {
        'need_nexus': True,
        'name_keywords': [],
        'path_keywords': ['MindStudio_*']
    },
    'docker_images': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['docker_images']
    },
    'sys_pkg': {
        'need_nexus': True,
        'name_keywords': [],
        'path_keywords': ['sources']
    },
    'gcc': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['sources']
    },
    'python': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['sources', 'pylibs']
    },
    'pytorch': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['sources', 'pylibs']
    },
    'tensorflow': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['sources', 'pylibs']
    },
    'ascend-device-plugin': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'ascend-docker-runtime': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'ascend-operator': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'clusterd': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'hccl-controller': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'mindio': {
        'need_nexus': False,
        'name_keywords': ['mindio', ],
        'path_keywords': ['run_from_mindio_zip', ],
    },
    'noded': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'npu-exporter': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'resilience-controller': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'volcano': {
        'need_nexus': False,
        'name_keywords': [],
        'path_keywords': ['mindxdl/dlPackage', 'mindxdl/baseImages'],
    },
    'fault-diag': {
        'need_nexus': False,
        'name_keywords': ['faultdiag'],
        'path_keywords': ['FaultDiag', 'pylibs'],
    },
}

pkg_run_paths = (
    [('Ascend-mindxdl-mindio',), 'run_from_mindio_zip'],
    [('Ascend-cann', 'Ascend-mindx', 'Atlas-A3-cann'), 'run_from_cann_zip'],
    [('Ascend-hdk-310p-npu-soc', 'Ascend-hdk-310p-npu-driver-soc',
      'Ascend-hdk-310p-npu-firmware-soc'), 'run_from_soc_zip'],
    [('A300i-pro', 'Atlas-300i-pro'), 'run_from_a300i_zip'],
    [('A300v-pro', 'Atlas-300v-pro'), 'run_from_a300v_pro_zip'],
    [('Atlas-300v',), 'run_from_a300v_zip'],
    [('A300i-duo', 'Atlas-300i-duo'), 'run_from_a300iduo_zip'],
    [('Ascend-hdk-310p', 'Ascend310P'), 'run_from_a310p_zip'],
    [('Ascend-hdk-310', 'Ascend310', 'A300-3000', 'A300-3010', 'Atlas-200'), 'run_from_infer_zip'],
    [('Ascend-hdk-910b', 'Ascend910B-hdk'), 'run_from_910b_zip'],
    [('A300t-9000', 'A800-9000', 'A800-9010', 'A900-9000'), 'run_from_train_zip'],
    [('Atlas-300t-pro',), 'run_from_train_pro_zip'],
    [('Ascend-hdk-910-npu', 'Ascend910'), 'run_from_910_zip'],
    [('Ascend-hdk-310b',), 'run_from_310b_zip'],
    [('Atlas-A3-hdk-npu',), 'run_from_910_93_zip'],
)

config_dir_map = {
    ('Ascend-mindxdl-mindio',): ('run_from_mindio_zip', '../templates/mindio'),
}


def get_keywords(tag, key):
    return tags_map.get(tag, {}).get(key, [])


def filter_pkg(pkg_file, tags):
    pkg_name = os.path.basename(pkg_file)
    for tag in tags:
        for keyword in get_keywords(tag, 'name_keywords'):
            if keyword in pkg_name:
                return True
    return False


def search_paths(base_dir, tags):
    paths = set()
    for tag in tags:
        for dir_type in get_keywords(tag, 'path_keywords'):
            for dir_path in glob.glob(os.path.join(base_dir, dir_type)):
                paths.add(dir_path)
    return paths


def get_run_dir(base_dir, filename):
    basename = os.path.basename(filename)
    for (prefix, dir_name) in pkg_run_paths:
        if basename.startswith(prefix):
            run_dir = os.path.join(base_dir, dir_name)
            return run_dir


def get_config_dir(base_dir, filename):
    basename = os.path.basename(filename)
    for prefix, (dir_name, source_dir) in config_dir_map.items():
        if basename.startswith(prefix):
            target_dir = os.path.join(base_dir, dir_name)
            return target_dir, os.path.join(base_dir, source_dir)
    return "", ""


def need_nexus(tags):
    for tag in tags:
        if tags_map.get(tag, {}).get('need_nexus'):
            return True
    return False
