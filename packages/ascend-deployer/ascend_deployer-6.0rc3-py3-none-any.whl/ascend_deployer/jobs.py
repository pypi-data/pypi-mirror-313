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
import codecs
import getpass
import glob
import importlib
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from threading import Thread
from zipfile import ZipFile, BadZipfile
from utils import compare_version

import utils
from module_utils.common_info import get_os_and_arch
from scripts import nexus
from scripts.pkg_utils import filter_pkg, search_paths, get_run_dir, get_config_dir, need_nexus, tags_map

LOG = logging.getLogger("ascend_deployer.jobs")


def prompt(tip):
    sys.stdout.write(tip)
    sys.stdout.flush()
    if platform.system() == 'Windows':
        import msvcrt
        answer = msvcrt.getch().decode('utf-8')
        print(answer)
        return answer
    fd = sys.stdin.fileno()
    if not os.isatty(fd):  # handle pipe
        answer = sys.stdin.read().strip()
        print(answer)
        return answer
    import tty
    import termios
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO  # 设置lflag, 禁用标准输入和回显模式
    try:
        tty.setraw(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        answer = sys.stdin.read(1)
        print(answer)
        return answer
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def accept_eula():
    eula_file = 'eula_en.txt'
    if 'zh_CN' in os.environ.get('LANG', ''):
        eula_file = 'eula_cn.txt'
    eula_file_path = os.path.join(utils.ROOT_PATH, 'scripts', eula_file)
    with codecs.open(eula_file_path, encoding='utf-8') as f:
        content = f.read()
        print(content if isinstance(content, str) else codecs.encode(content, 'utf-8'))
    answer = prompt("Do you accept the EULA to use Ascend-deployer?[y/N]")
    return len(answer) == 1 and answer.lower() == 'y'


def start_nexus(ip, port):
    if os.path.exists(utils.NEXUS_SENTINEL_FILE):
        os.unlink(utils.NEXUS_SENTINEL_FILE)
        LOG.info('unlink existed sentinel file: {}'.format(utils.NEXUS_SENTINEL_FILE))
    try:
        nexus.main(ip, port)
        LOG.info('start nexus({}:{}) successfully'.format(ip, port))
        dir_path = os.path.dirname(utils.NEXUS_SENTINEL_FILE)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, 0o700)
        with open(utils.NEXUS_SENTINEL_FILE, 'w'):
            pass
        LOG.info('set sentinel file: {}'.format(utils.NEXUS_SENTINEL_FILE))
    except Exception as e:
        LOG.error('start nexus failed: {}'.format(e))


def get_localhost_ip():
    host_file = os.path.join(utils.ROOT_PATH, 'inventory_file')
    host_lines = []
    with open(host_file) as f:
        host_lines = f.readlines()

    for line in host_lines:
        if line.startswith("RUNNER_IP="):
            host_ip = line.replace("RUNNER_IP=", '').replace('"', '').strip()
            if host_ip:
                return host_ip

    ssh_connection_info = os.environ.get("SSH_CONNECTION", '').split()
    if len(ssh_connection_info) > 2:
        return ssh_connection_info[2]

    first_ip = ''
    for line in host_lines:
        line = line.strip()
        if line.startswith('#') or 'ansible_' not in line:
            continue
        host = line.split()[0]
        if host != 'localhost':
            first_ip = host
            break
    if not first_ip:
        return '127.0.0.1'
    if ':' in first_ip:
        net_prefix = first_ip.split(':')[0]
        ver = '-6'
    else:
        net_prefix = first_ip.split('.')[0]
        ver = '-4'
    lines = utils.run_cmd('ip {} address'.format(ver), stdout=subprocess.PIPE)
    for line in lines:
        line = line.strip()
        if 'inet' not in line or ' ' not in line:
            continue
        ip = line.split()[1].split('/')[0]
        if ip.startswith(net_prefix):
            return ip
    return '127.0.0.1'


def get_nexus_url(ip, port):
    host = '[{}]'.format(ip) if ':' in ip else ip
    return 'http://{}:{}'.format(host, port)


class AnsibleJob(object):
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file

    @staticmethod
    def get_inventory_file():
        return os.path.join(utils.ROOT_PATH, 'inventory_file')

    @staticmethod
    def handle_python_env(args):
        ascend_python_version = os.environ.get("ASCEND_PYTHON_VERSION")
        if not ascend_python_version:
            config_file = os.path.join(utils.ROOT_PATH, 'downloader', 'config.ini')
            try:
                import configparser
                cfp = configparser.ConfigParser()
            except ImportError:
                import ConfigParser
                cfp = ConfigParser.SafeConfigParser()
            cfp.read(config_file)
            ascend_python_version = cfp.get('python', 'ascend_python_version')
        version_list = utils.get_python_version_list()
        if ascend_python_version not in version_list:
            raise Exception("ASCEND_PYTHON_VERSION is not available, "
                            "available python version list is {}".format(version_list))
        version = ascend_python_version.replace('P', 'p').replace('-', '')
        args.extend([
            '-e', 'python_tar={}'.format(ascend_python_version),
            '-e', 'python_version={}'.format(version),
        ])

    def run_playbook(self, input_tags, no_copy=False, only_copy=False, envs=None, ansible_args=None):
        facts_path = os.path.join(utils.ROOT_PATH, 'facts_cache')
        if os.path.exists(facts_path):
            shutil.rmtree(facts_path)
        args = self.build_args(envs)
        skip_tags = []
        tags = list(input_tags) if isinstance(input_tags, list) else input_tags
        if tags:
            if not isinstance(tags, list):
                tags = [tags]
            if 'all' in tags:
                tags[tags.index('all')] = 'whole'  # all is ansible reserved tag
            if 'copy_pkgs' in tags:  # copy_pkgs仅作为拷贝包的依据，不参与实际部署
                tags.remove('copy_pkgs')
            if only_copy:
                skip_tags.extend(tags)
            if no_copy:
                skip_tags.append('copy')
            else:
                tags.append('copy')
            args.extend(['--tags', ','.join(tags)])
            if skip_tags:
                args.extend(['--skip-tags', ','.join(skip_tags)])
        if ansible_args:
            args.extend(ansible_args)
        return utils.run_cmd(args)

    def build_args(self, envs):
        inventory_file = self.get_inventory_file()
        args = ['ansible-playbook', '-i', inventory_file, self.yaml_file]
        if not envs:
            envs = {}
        self.handle_python_env(args)
        for k, v in envs.items():
            args.extend(['-e', '{}={}'.format(k, v)])
        return args

    def run_ansible(self, run_args):
        inventory_file = self.get_inventory_file()
        args = ['ansible', '-i', inventory_file]
        args.extend(run_args)
        return utils.run_cmd(args)


process_path = os.path.join(utils.ROOT_PATH, 'playbooks', 'process')
process_install = AnsibleJob(os.path.join(process_path, 'process_install.yml')).run_playbook
process_scene = AnsibleJob(os.path.join(process_path, 'process_scene.yml')).run_playbook
process_patch = AnsibleJob(os.path.join(process_path, 'process_patch.yml')).run_playbook
process_patch_rollback = AnsibleJob(os.path.join(process_path, 'process_patch_rollback.yml')).run_playbook
process_test = AnsibleJob(os.path.join(process_path, 'process_test.yml')).run_playbook
process_check = AnsibleJob(os.path.join(process_path, 'process_check.yml')).run_playbook
process_clean = AnsibleJob(None).run_ansible
process_hccn = AnsibleJob(os.path.join(process_path, 'process_hccn.yml')).run_playbook
process_hccn_check = AnsibleJob(os.path.join(process_path, 'process_hccn_check.yml')).run_playbook


class PrepareJob(object):
    def __init__(self):
        self.pip_path = os.path.join(utils.ROOT_PATH, 'resources', 'pylibs', 'pip*.whl')
        self.cache_dir = os.path.join(utils.ROOT_PATH, 'resources', 'pylibs')
        self.rc_file = os.path.expanduser('~/.local/ascend_deployer_rc')
        self.os_ver_arch = get_os_and_arch()

    def pip_install(self, pkg):
        cmd_args = [sys.executable]
        cmd_args.extend(['-m', 'pip', 'install', '-U'])
        cmd_args.extend(pkg)
        cmd_args.extend(['--no-index', '--find-links', self.cache_dir])
        return utils.run_cmd(cmd_args, oneline=True)

    def update_env_file(self):
        bin_path = os.path.dirname(sys.executable)
        lib_path = os.path.dirname(os.path.dirname(os.__file__))
        lines = [
            "export ANSIBLE_CONFIG={}\n".format(os.path.join(utils.ROOT_PATH, 'ansible.cfg')),
            "export PYTHONWARNINGS=ignore::UserWarning\n",
            "export PATH={}:~/.local/bin:$PATH\n".format(bin_path),
            "export LD_LIBRARY_PATH={}:~/.local/lib:$LD_LIBRARY_PATH\n".format(lib_path)
        ]
        rc_dir = os.path.dirname(self.rc_file)
        if not os.path.exists(rc_dir):
            os.makedirs(rc_dir, mode=0o750)
        with open(self.rc_file, 'w') as f:
            f.writelines(lines)

    @staticmethod
    def find_first(pattern):
        files = glob.glob(pattern)
        if not files:
            raise Exception("no {} found, forget to download firstly?".format(pattern))
        return files[0]

    def install_distutils(self):
        try:
            importlib.import_module('distutils.util')
        except ImportError:  # exist on Ubuntu 18.04
            pkg_path = os.path.join(utils.ROOT_PATH, 'resources', self.os_ver_arch, 'python*-distutils*')
            cmd = 'dpkg --force-all -i {}'.format(self.find_first(pkg_path))
            utils.run_cmd(cmd, oneline=True)

    def install_pip(self):
        need_install = False
        try:
            pip = importlib.import_module('pip')
        except ImportError:
            need_install = True
        else:
            major_version = int(getattr(pip, '__version__', '9.0.0').split('.')[0])
            if major_version < 20:
                need_install = True
        if not need_install:
            return
        pip_file = self.find_first(self.pip_path)
        install_pip_cmd_args = [sys.executable, '{}/pip'.format(pip_file), 'install', '-U', pip_file]
        utils.run_cmd(install_pip_cmd_args, oneline=True)

    def install_ansible(self):
        try:
            import ansible
            return
        except ImportError:
            self._install_by_version()
            self.update_env_file()
        site = importlib.import_module('site')
        try:
            reload(site)
        except NameError:
            importlib.reload(site)

    def ensure_docker_daemon_exist(self):
        docker_daemon = "/etc/docker/daemon.json"
        if os.path.exists(docker_daemon):
            return
        content_dict = dict()
        from distutils.spawn import find_executable
        if not find_executable('rpm'):
            content_dict.update({
                "exec-opts": ["native.cgroupdriver=systemd"],
                "live-restore": True
            })
        elif self.os_ver_arch.startswith('OpenEuler'):
            content_dict.update({
                "live-restore": True
            })
        docker_config_path = os.path.dirname(docker_daemon)
        if not os.path.exists(docker_config_path):
            os.makedirs(docker_config_path, mode=0o750)
        with open(docker_daemon, 'w') as f:
            json.dump(content_dict, f, indent=4)

    def install_docker(self):
        utils.install_pkg('docker', self.os_ver_arch, 'docker', '*')
        if getpass.getuser() == 'root':
            self.ensure_docker_daemon_exist()
            utils.run_cmd("systemctl enable docker")
            utils.run_cmd("systemctl daemon-reload")
            utils.run_cmd("systemctl restart docker")

    def install_selinux(self):
        if not self.os_ver_arch.startswith(('OpenEuler', 'Kylin', "CULinux")):
            return
        try:
            importlib.import_module('selinux')
        except ImportError:
            utils.install_pkg('selinux', self.os_ver_arch, 'libselinux*')
            if self.os_ver_arch.startswith('OpenEuler_22.03'):
                utils.install_pkg('selinux', self.os_ver_arch, 'libsepol*')
                utils.install_pkg('selinux', self.os_ver_arch, 'pcre2*')

    def install_openssl(self):
        if self.os_ver_arch.startswith('CentOS'):
            utils.install_pkg('openssl11', self.os_ver_arch, 'openssl*')
            utils.install_pkg('perl', self.os_ver_arch, 'perl*')

    def install_haveged(self):
        if utils.install_pkg('haveged', self.os_ver_arch, '*havege*') is not None:
            utils.run_cmd('systemctl enable haveged')
            utils.run_cmd('systemctl restart haveged')

    def install_basic_dependencies(self):
        utils.install_pkg('bzip2', self.os_ver_arch, 'bzip2*')
        utils.install_pkg('unzip', self.os_ver_arch, 'unzip*')
        utils.install_pkg('tar', self.os_ver_arch, 'tar*')
        utils.install_pkg('sshpass', self.os_ver_arch, 'sshpass*')
        if "Debian" in self.os_ver_arch:
            packages = ['iptables', 'gnupg', 'gpg', 'libassuan', 'dirmngr', 'gnupg-l10n', 'gnupg-utils', 'gpg-agent',
                        'gpgconf', 'gpgsm', 'gpg-wks-client', 'gpg-wks-server', 'libnpth0', 'libksba8',
                        'pinentry-curses', 'slirp4netns', 'python3-lib2to3', ]
            for package in packages:
                utils.install_pkg(package, self.os_ver_arch, '{}*'.format(package))
        self.install_haveged()
        self.install_selinux()
        self.install_openssl()

    def run(self):
        self.install_distutils()
        self.install_pip()
        self.install_ansible()
        self.install_basic_dependencies()

    def _install_by_version(self):
        cur_version_big = '.'.join(sys.version.split('.')[:2])
        for py_ver, packages in self._get_python_packages().items():
            # eg: cp311 -> 3.11
            py_ver_in_number = py_ver[2] + '.' + py_ver[3:]
            if compare_version(py_ver_in_number, cur_version_big) == 0:
                if "Ubuntu_18.04" in self.os_ver_arch:
                    packages = [pkg for pkg in packages if "pyyaml" not in pkg.lower()]
                self.pip_install(packages)
                break

    def _get_python_packages(self):
        basic_path = os.path.dirname(__file__)
        ansible_require_file = os.path.join(basic_path, 'downloader/ansible_reqs.json')
        with open(ansible_require_file) as f:
            reqs = json.load(f)
            return reqs


class TempDir(object):
    def __init__(self, **kwargs):
        dir_path = kwargs.get('dir')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, 0o700)
        self.name = tempfile.mkdtemp(**kwargs)

    def __enter__(self):
        return self.name

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.name)


class ResourcePkg(object):
    def __init__(self, tags=None, need_copy_all_pkgs=False):
        self.tags = []
        if tags:
            self.tags = [tags] if isinstance(tags, str) else tags
        # 当选择copy_pkgs选项时，复制所有包，不依赖
        self.need_copy_tags = list(tags_map.keys()) if need_copy_all_pkgs else self.tags
        self.resource_path = os.path.join(utils.ROOT_PATH, 'resources')
        self.root_ca = os.path.join(utils.ROOT_PATH, 'scripts', 'Huawei_Software_Integriry_Protection_Root_CA.pem')
        self.root_ca_g2 = os.path.join(utils.ROOT_PATH, 'scripts', 'Huawei_Integrity_Root_CA_G2.pem')
        self.tmp_dir = os.path.expanduser('~/.tmp')
        if getpass.getuser() == 'root':
            self.ascend_cert = '/usr/local/Ascend/toolbox/latest/Ascend-DMI/bin/ascend-cert'
            self.sys_crl_file = '/etc/hwsipcrl/ascendsip.crl'
            self.sys_g2_crl_file = '/etc/hwsipcrl/ascendsip_g2.crl'
        else:
            self.ascend_cert = os.path.expanduser('~/Ascend/toolbox/latest/Ascend-DMI/bin/ascend-cert')
            self.sys_crl_file = os.path.expanduser('~/.local/hwsipcrl/ascendsip.crl')
            self.sys_g2_crl_file = os.path.expanduser('~/.local/hwsipcrl/ascendsip_g2.crl')
        self.arches = set()

    def handle_run_pkg(self, file):
        run_dir = get_run_dir(self.resource_path, file)
        config_dir, config_source_dir = get_config_dir(self.resource_path, file)
        if config_dir:
            shutil.copytree(config_source_dir, config_dir)
        if run_dir:
            if not os.path.exists(run_dir):
                os.makedirs(run_dir, 0o750)
            shutil.copy(file, os.path.join(run_dir, os.path.basename(file)))

    @staticmethod
    def _extract_filter_rule(filename, members):
        filename = os.path.splitext(os.path.basename(filename))[0]
        if any(p for p in members if p.endswith('.cms')):
            members = [p for p in members if p.startswith(filename)]
        return members

    @staticmethod
    def extract_zip(file, path, filter_rule=None):
        try:
            with ZipFile(file) as z:
                members = z.namelist()
                if filter_rule:
                    members = filter_rule(file, members)
                z.extractall(path, members)
                return members
        except BadZipfile:
            raise Exception('{} is corrupted'.format(file))

    @staticmethod
    def extract_tar(file, path):
        try:
            with tarfile.open(file) as f:
                members = f.getmembers()
                f.extractall(path, members)
                return members
        except tarfile.TarError:
            raise Exception('{} is corrupted'.format(file))

    def extract(self, file, path):
        if not os.path.exists(path):
            os.makedirs(path, 0o750)
        if file.endswith('.zip'):
            if "faultdiag" in file:
                return self.extract_zip(file, path)
            else:
                return self.extract_zip(file, path, self._extract_filter_rule)
        elif file.endswith('.tar.gz'):
            return self.extract_tar(file, path)
        else:
            raise Exception('Unsupported to extract file: {}'.format(file))

    @staticmethod
    def update_crl(old_crl, new_crl):
        dir_path = os.path.dirname(new_crl)
        if not os.path.exists(dir_path):
            LOG.info('create sys crl dir: {}'.format(dir_path))
            os.makedirs(dir_path, 0o700)
        LOG.info('create sys crl file: {}'.format(new_crl))
        shutil.copy(old_crl, new_crl)

    @staticmethod
    def verify_crl(crl_file, ca_file):
        x509 = importlib.import_module('cryptography.x509')
        backends = importlib.import_module('cryptography.hazmat.backends')
        crl = x509.load_der_x509_crl(open(crl_file, 'rb').read(), backends.default_backend())
        ca = x509.load_pem_x509_certificate(open(ca_file, 'rb').read(), backends.default_backend())
        if not crl.is_signature_valid(ca.public_key()):
            raise Exception('invalid signature for crl: {}'.format(crl_file))
        if crl.get_revoked_certificate_by_serial_number(ca.serial_number):
            raise Exception('ca_file: {} is revoked'.format(ca_file))
        return crl

    @staticmethod
    def clean(ip):
        try:
            if os.path.exists(utils.NEXUS_SENTINEL_FILE):
                os.unlink(utils.NEXUS_SENTINEL_FILE)
                LOG.info('clean sentinel file: {}'.format(utils.NEXUS_SENTINEL_FILE))
            utils.run_cmd('docker rm -f nexus', stdout=subprocess.PIPE)
            nexus_data_path = '/tmp/nexus-data'
            if os.path.exists(nexus_data_path):
                utils.run_cmd('umount {}'.format(nexus_data_path))
                shutil.rmtree(nexus_data_path)
            if ':' in ip:
                utils.run_cmd('docker network rm ip6net_nexus', stdout=subprocess.PIPE)
        except Exception as e:
            LOG.warning('clean nexus meet issue: {}'.format(e))

    def compare_crl(self, crl_file, sys_crl_file, ca_file):
        zip_crl = self.verify_crl(crl_file, ca_file)
        if os.path.exists(sys_crl_file):
            sys_crl = self.verify_crl(sys_crl_file, ca_file)
            return zip_crl.last_update > sys_crl.last_update
        return True

    def verify_cms(self, crl_file, sys_crl_file, ca_file, cms_file, data_file):
        if self.compare_crl(crl_file, sys_crl_file, ca_file):
            self.update_crl(crl_file, sys_crl_file)
        from distutils.spawn import find_executable
        openssl = find_executable('openssl11') or 'openssl'
        cmd = '{} cms -verify --no_check_time -in {} -inform DER -CAfile {} -binary -content {}' \
              ' -purpose any -out {}'.format(openssl, cms_file, ca_file, data_file, os.devnull)
        utils.run_cmd(cmd, stderr=os.open(os.devnull, os.O_RDWR))

    def verify_hmac(self, data_file, crl_file):
        cms_file = data_file + '.cms'
        for item in (cms_file, data_file, crl_file):
            os.chmod(item, 0o600)
        if os.path.exists(self.ascend_cert):
            update_crl_cmd = '{} -u {}'.format(self.ascend_cert, crl_file)
            utils.run_cmd(update_crl_cmd, stdout=os.open(os.devnull, os.O_RDWR), stderr=os.open(os.devnull, os.O_RDWR))
            verify_cmd = '{} {} {} {}'.format(self.ascend_cert, cms_file, data_file, crl_file)
            utils.run_cmd(verify_cmd, stdout=os.open(os.devnull, os.O_RDWR), stderr=os.open(os.devnull, os.O_RDWR))
            return
        try:
            self.verify_cms(crl_file, self.sys_g2_crl_file, self.root_ca_g2, cms_file, data_file)
        except Exception as e:
            LOG.warning(e)
            self.verify_cms(crl_file, self.sys_crl_file, self.root_ca, cms_file, data_file)

    @staticmethod
    def _get_crl_file(crl_files, tmp_file):
        same_name_crl_files = [crl_file for crl_file in crl_files if crl_file.replace(".crl", "") in tmp_file]
        if same_name_crl_files:
            crl_file = same_name_crl_files[0]
        else:
            crl_file = crl_files[0]
        return crl_file

    def handle_zip_pkg(self, file):
        with TempDir(dir=self.tmp_dir) as tmp_path:
            # first unzip
            members = self.extract(file, tmp_path)
            cms_files = [x for x in members if x.endswith('.cms')]
            crl_files = [x for x in members if x.endswith('.crl')]
            if not cms_files or not crl_files:
                file_name = file.split("/")[-1]
                if "auto" in self.tags or file_name.startswith("Ascend-mindxdl-"):
                    LOG.info('no .cms or .crl found, skip to handle {}'.format(file))
                    return
                LOG.error('{} is corrupted, does not have cms or crl file'.format(file))
                raise Exception('{} is corrupted, does not have cms or crl file'.format(file))
            tmp_file = os.path.join(tmp_path, os.path.splitext(cms_files[0])[0])
            crl_file = self._get_crl_file(crl_files, tmp_file)
            crl_file_path = os.path.join(tmp_path, crl_file)
            # verify hmac
            self.verify_hmac(tmp_file, crl_file_path)
            # second unzip
            if tmp_file.endswith("zip"):
                run_dir = get_run_dir(self.resource_path, tmp_file)
                self.extract(tmp_file, run_dir)
            elif "faultdiag" in tmp_file:
                fault_diag_dir = os.path.join(self.resource_path, "FaultDiag")
                if not os.path.exists(fault_diag_dir):
                    os.makedirs(fault_diag_dir, 0o750)
                for cms_file in cms_files:
                    tmp_whl_file = os.path.join(tmp_path, os.path.splitext(cms_file)[0])
                    shutil.copy(tmp_whl_file, fault_diag_dir)

    def iter_files(self, suffix):
        for root, dirs, files in os.walk(self.resource_path):
            for file in files:
                for keyword in ('x86_64', 'amd64'):
                    if keyword in file:
                        self.arches.add('x86_64')
                if 'aarch64' in file:
                    self.arches.add('aarch64')
                src_file = os.path.join(root, file)
                if src_file.endswith(suffix) and filter_pkg(src_file, self.need_copy_tags):
                    yield src_file

    def extract_pkgs(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
        for cache_dir in glob.glob(os.path.join(self.resource_path, 'run_from_*_zip')):
            shutil.rmtree(cache_dir)
        for src_file in self.iter_files('.run'):
            self.handle_run_pkg(src_file)
        for src_file in self.iter_files('.zip'):
            self.handle_zip_pkg(src_file)

    def iter_need_pack_files(self, arch):
        exclude_arch = 'aarch64' if arch == 'x86_64' else 'x86_64'
        for dir_path in search_paths(self.resource_path, self.need_copy_tags):
            if os.path.isfile(dir_path):
                yield dir_path
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if exclude_arch not in file:
                        yield os.path.join(root, file)

    def pack(self, tar_file, arch):
        with tarfile.open(tar_file, 'w') as tar:
            for file in self.iter_need_pack_files(arch):
                tar.add(file, arcname=file.replace(utils.ROOT_PATH, ''))

    def pack_pkgs(self):
        for arch in self.arches:
            tar_file = os.path.join(os.path.expanduser('~/resources_{}.tar'.format(arch)))
            if os.path.exists(tar_file):
                os.unlink(tar_file)
            self.pack(tar_file, arch)

    def handle_pkgs(self):
        print("Extracting and repacking packages...")
        self.extract_pkgs()
        self.pack_pkgs()

    def start_nexus_daemon(self, ip, port=58081):
        if not need_nexus(self.tags):
            return

        if getpass.getuser() != 'root':
            LOG.warning('not support to start nexus for by non-root user, please switch to root user')
            return
        PrepareJob().install_docker()
        thread = Thread(target=start_nexus, args=(ip, port))
        thread.daemon = True
        thread.start()
        return get_nexus_url(ip, port)
