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
import json
import shlex
import stat
import sys
import argparse
import getpass
import logging
import logging.handlers
import platform
import shutil
import re
from subprocess import PIPE, Popen

ROOT_PATH = SRC_PATH = os.path.dirname(__file__)
NEXUS_SENTINEL_FILE = os.path.expanduser('~/.local/nexus.sentinel')
MODE_700 = stat.S_IRWXU
MODE_600 = stat.S_IRUSR | stat.S_IWUSR
MODE_400 = stat.S_IRUSR

LOG = logging.getLogger('ascend_deployer.utils')
MAX_LEN = 120

dir_list = ['downloader', 'playbooks', 'tools', 'ansible_plugin', 'group_vars', 'patch', 'scripts', 'yamls',
            'library', 'module_utils', 'templates']
file_list = ['install.sh', 'inventory_file', 'ansible.cfg',
             '__init__.py', 'ascend_deployer.py', 'jobs.py', 'utils.py',
             'version.json']

VERSION_PATTERN = re.compile(r"(\d+)")


def compare_version(src_version, target_version):
    use_version_parts = VERSION_PATTERN.split(src_version)
    new_version_parts = VERSION_PATTERN.split(target_version)
    for cur_ver_part, new_ver_part in zip(use_version_parts, new_version_parts):
        if cur_ver_part.isdigit() and new_ver_part.isdigit():
            result = int(cur_ver_part) - int(new_ver_part)
        else:
            result = (cur_ver_part > new_ver_part) - (cur_ver_part < new_ver_part)
        if result != 0:
            return result
    return len(use_version_parts) - len(new_version_parts)

def copy_scripts():
    """
    copy scripts from library to ASCEND_DEPLOY_HOME
    the default ASCEND_DEPLOYER_HOME is HOME
    """
    if SRC_PATH == ROOT_PATH:
        return

    if not os.path.exists(ROOT_PATH):
        os.makedirs(ROOT_PATH, mode=0o750)
    for dir_name in dir_list:
        src = os.path.join(SRC_PATH, dir_name)
        dst = os.path.join(ROOT_PATH, dir_name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copytree(src, dst)

    for filename in file_list:
        src = os.path.join(SRC_PATH, filename)
        dst = os.path.join(ROOT_PATH, filename)
        if not os.path.exists(dst) and os.path.exists(src):
            shutil.copy(src, dst)


if 'site-packages' in ROOT_PATH or 'dist-packages' in ROOT_PATH:
    deployer_home = os.getcwd()
    if platform.system() == 'Linux':
        deployer_home = os.getenv('ASCEND_DEPLOYER_HOME', os.getenv('HOME'))
    ROOT_PATH = os.path.join(deployer_home, 'ascend-deployer')
    copy_scripts()


class ValidChoices(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, list(set(values)))


class SkipCheck(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if value.lower() == "true":
            setattr(namespace, self.dest, True)
            return
        setattr(namespace, self.dest, False)


def pretty_format(text):
    results = []
    loc = text.index(':') + 1
    results.append(text[:loc])
    results.extend(text[loc:].split(','))
    return results


class HelpFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if ':' in text:
            return pretty_format(text)
        import textwrap
        return textwrap.wrap(text, width, break_on_hyphens=False)


def args_with_comma(args):
    new_args = []
    for arg in args:
        sep_loc = arg.find('=')
        ver_loc = arg.find('==')
        if sep_loc > 0 and sep_loc != ver_loc:
            new_args.append(arg[:sep_loc])
            arg = arg[sep_loc + 1:]
        for sub_arg in arg.split(','):
            if sub_arg:
                new_args.append(sub_arg)
    return new_args


os_items = sorted(os.listdir(os.path.join(ROOT_PATH, "downloader", "config")))
pkg_file_list = os.listdir(os.path.join(ROOT_PATH, "downloader", "software"))
pkg_items = set()
for pkg_file in pkg_file_list:
    pkg_name, version = pkg_file.split('_')
    pkg_items.add(pkg_name)
    pkg_items.add('{}=={}'.format(pkg_name, version.replace('.json', '')))
pkg_items = sorted(pkg_items)


def get_python_version_list():
    python_version_json = os.path.join(ROOT_PATH, 'downloader', 'python_version.json')
    with open(python_version_json, 'r') as json_file:
        data = json.load(json_file)
        available_python_list = [item['filename'].rstrip('.tar.xz') for item in data]
        return available_python_list


def get_name_list(dir_path, prefix, suffix):
    items = []
    for file_name in os.listdir(dir_path):
        if file_name.startswith(prefix) and file_name.endswith(suffix):
            item = file_name.replace(prefix, '').replace(suffix, '')
            items.append(item)
    return sorted(items)


dl_items = ['ascend-device-plugin', 'ascend-docker-runtime', 'ascend-operator', 'hccl-controller', 'mindio', 'noded',
            'npu-exporter', 'resilience-controller', 'volcano', 'clusterd', 'dl']
install_items = get_name_list(os.path.join(ROOT_PATH, "playbooks", "install"), 'install_', '.yml')
scene_items = get_name_list(os.path.join(ROOT_PATH, "playbooks", "scene"), 'scene_', '.yml')
patch_items = get_name_list(os.path.join(ROOT_PATH, "playbooks", "install", "patch"), "install_", ".yml")
test_items = ['all', 'firmware', 'driver', 'nnrt', 'nnae', 'toolkit', 'toolbox', 'mindspore', 'pytorch',
              'tensorflow', 'tfplugin', 'fault-diag', 'ascend-docker-runtime', 'ascend-device-plugin', 'volcano',
              'noded', 'clusterd', 'hccl-controller', 'ascend-operator', 'npu-exporter', 'resilience-controller']

LOG_MAX_BACKUP_COUNT = 5
LOG_MAX_SIZE = 20 * 1024 * 1024
LOG_FILE = os.path.join(ROOT_PATH, 'install.log')
LOG_OPERATION_FILE = os.path.join(ROOT_PATH, 'install_operation.log')


class UserHostFilter(logging.Filter):
    user = getpass.getuser()
    host = os.getenv('SSH_CLIENT', 'localhost').split()[0]

    def filter(self, record):
        record.user = self.user
        record.host = self.host
        return True


class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self):
        try:
            os.chmod(self.baseFilename, 0o400)
        except OSError:
            os.chmod('{}.{}'.format(self.baseFilename, LOG_MAX_BACKUP_COUNT), 0o600)
        finally:
            logging.handlers.RotatingFileHandler.doRollover(self)
            os.chmod(self.baseFilename, 0o600)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        'extra': {
            'format': "%(asctime)s %(user)s@%(host)s [%(levelname)s] "
                      "[%(filename)s:%(lineno)d %(funcName)s] %(message)s"
        }
    },
    "filters": {
        "user_host": {
            '()': UserHostFilter
        }
    },
    "handlers": {
        "install": {
            "level": "DEBUG",
            "formatter": "extra",
            "class": 'utils.RotatingFileHandler',
            "filename": LOG_FILE,
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_MAX_BACKUP_COUNT,
            'encoding': "UTF-8",
            "filters": ["user_host"],
        },
        "install_operation": {
            "level": "INFO",
            "formatter": "extra",
            "class": 'utils.RotatingFileHandler',
            "filename": LOG_OPERATION_FILE,
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_MAX_BACKUP_COUNT,
            'encoding': "UTF-8",
            "filters": ["user_host"],
        },
    },
    "loggers": {
        "ascend_deployer": {
            "handlers": ["install"],
            "level": "INFO",
            "propagate": True,
        },
        "install_operation": {
            "handlers": ["install_operation"],
            "level": "INFO",
            "propagate": True,
        },
    }
}


def run_cmd(args, oneline=False, **kwargs):
    if not kwargs.get('shell') and isinstance(args, str):
        args = shlex.split(args, posix=platform.system() == 'Linux')
    cmd = args if isinstance(args, str) else ' '.join(args)
    LOG.info(cmd.center(MAX_LEN, '-'))
    stdout = kwargs.pop('stdout', PIPE if oneline else None)
    stderr = kwargs.pop('stderr', PIPE)
    text = kwargs.pop('universal_newlines', True)
    output = []
    process = Popen(args, stdout=stdout, stderr=stderr, universal_newlines=text, **kwargs)
    if oneline:
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            output.append(line)
            LOG.info(line)
            if len(line) <= MAX_LEN:
                line += (MAX_LEN - len(line)) * " "
            else:
                # if the line too long(> MAX_LEN), only print first (MAX_LEN -3) characters and '...'
                line = line[0:MAX_LEN - 4] + "..."
            sys.stdout.write("\r{}".format(line))
        err = process.stderr.read()
        process.wait()
    else:
        out, err = process.communicate()
        if isinstance(out, str):
            output = out.splitlines()
            for line in output:
                LOG.info(line)
    if process.returncode:
        if err and '[ASCEND][WARNING]' not in str(err):
            raise Exception(err)
        raise Exception("returned non-zero exit status {}".format(process.returncode))
    elif err and '[ASCEND][WARNING]' in str(err):
        print(err)
    return output


def install_pkg(name, *paths):
    from distutils.spawn import find_executable
    if find_executable(name):
        LOG.info('{} is already installed, skip'.format(name))
        return
    if find_executable('dpkg'):
        prefix_cmd = "dpkg --force-all -i"
        suffix_cmd = '.deb'
    else:
        prefix_cmd = "rpm -ivUh --force --nodeps --replacepkgs"
        suffix_cmd = '.rpm'
    pkg_path = os.path.join(ROOT_PATH, 'resources', *paths)
    if not pkg_path.endswith(('.deb', '.rpm')):
        pkg_path += suffix_cmd
    cmd = "{} {}".format(prefix_cmd, pkg_path)
    if getpass.getuser() != 'root':
        raise Exception('no permission to run cmd: {}, please run command with root user firstly'.format(cmd))
    return run_cmd(cmd, oneline=True, shell=True)


def get_hosts_name(tags):
    if (isinstance(tags, str) and tags in dl_items) or (isinstance(tags, list) and set(tags) & set(dl_items)):
        return 'master,worker'
    return 'worker'
