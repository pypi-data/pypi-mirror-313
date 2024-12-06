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
import base64
import glob
import json
import logging
import os
import platform
import random
import shlex
import shutil
import string
import subprocess
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import ROOT_PATH

try:
    from urllib.parse import urljoin
    from urllib.request import Request, urlopen

    PY3 = True
except ImportError:
    from urllib2 import Request, urlopen
    from urlparse import urljoin

    PY3 = False

LOG = logging.getLogger("ascend_deployer.scripts.nexus")


def get_passwd():
    rand = random.SystemRandom()
    return "".join(rand.choice(string.digits + string.ascii_letters) for _ in range(16))


class OsRepository:
    NEXUS_USER = "admin"
    nexus_passwd = get_passwd()
    gpg_passwd = get_passwd()

    def __init__(self, ip=None, port=58081):
        try:
            self.nexus_run_ip = ip or os.environ["SSH_CONNECTION"].split()[2]
            self.nexus_run_port = port
            self.working_on_ipv6 = False
            if ":" in self.nexus_run_ip:  # ipv6格式需要用括号包住域名部分
                self.nexus_run_ip = "[%s]" % self.nexus_run_ip
                self.working_on_ipv6 = True
        except KeyError:
            raise RuntimeError("Get environment variable SSH_CONNECTION failed,maybe switch users after SSH connection")
        self.nexus_url = "http://{}:{}".format(self.nexus_run_ip, self.nexus_run_port)
        self.config = "{}/scripts/nexus_config.json".format(ROOT_PATH)
        self.arch = platform.machine()
        os.environ.pop("http_proxy", "")
        os.environ.pop("https_proxy", "")
        with open(self.config, "r") as f:
            self.config_content = json.load(f)
        self.nexus_data_dir = os.path.join("/tmp", "nexus-data")
        self.nexus_image_name = self.config_content.get("image")
        nexus_dir = os.path.join(ROOT_PATH, "resources", "nexus")
        try:
            self.nexus_image = glob.glob("{}/nexus*{}.tar".format(nexus_dir, self.arch))[0]
        except IndexError:
            raise RuntimeError(
                "The nexus image does not exist. Ensure that the nexus image is in the {} directory.".format(nexus_dir)
            )
        auth = base64.b64encode("{}:{}".format(self.NEXUS_USER, self.nexus_passwd).encode()).decode()
        self.post_headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic {}".format(auth),
        }
        self.upload_headers = {
            "Authorization": "Basic {}".format(auth),
            "Content-Type": "application/octet-stream",
        }

    @staticmethod
    def _run_cmd(cmd, ignore_errors=False, log=True):
        if log:
            LOG.info("nexus: {}".format(cmd).center(120, "-"))
        result = subprocess.Popen(
            shlex.split(cmd),
            shell=False,
            universal_newlines=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        out, err = result.communicate()
        if result.returncode != 0 and not ignore_errors:
            raise RuntimeError("run cmd: {} failed, reason: {}".format(cmd, err))
        if log:
            for line in out.splitlines():
                if isinstance(line, bytes):
                    # Convert `line` to Unicode if it's a byte string
                    try:
                        line = line.decode('utf-8')
                    except UnicodeDecodeError:
                        LOG.info("Error: Unable to decode the byte string using UTF-8")
                        continue
                LOG.info(line)
        return out, err

    @staticmethod
    def _run_request(url, data, headers, method, timeout=20):
        if PY3:
            req = Request(url=url, data=data, headers=headers, method=method)
        else:
            req = Request(url=url, data=data, headers=headers)
            req.get_method = lambda: method
        urlopen(req, timeout=timeout)

    def init_nexus(self):
        self._run_nexus()
        self._check_nexus_status()
        tmp_passwd_file = "{}/admin.password".format(self.nexus_data_dir)
        with open(tmp_passwd_file, "r") as f:
            old_passwd = f.read()
        auth = base64.b64encode("{}:{}".format(self.NEXUS_USER, old_passwd).encode()).decode()
        headers = {
            "accept": "application/json",
            "Content-Type": "text/plain",
            "Authorization": "Basic {}".format(auth),
        }
        url = "{}/service/rest/v1/security/users/admin/change-password".format(self.nexus_url)
        self._run_request(url, data=self.nexus_passwd.encode("utf-8"), headers=headers, method="PUT")

        url = "{}/service/rest/v1/security/anonymous".format(self.nexus_url)
        data = {
            "enabled": True,
            "userId": "anonymous",
            "realmName": "NexusAuthorizingRealm",
        }
        self._run_request(url, data=json.dumps(data).encode("utf-8"), headers=self.post_headers, method="PUT")

    @staticmethod
    def get_download_os_info():
        os_list_dir = "{}/resources".format(ROOT_PATH)
        os_list = [os_item for os_item in glob.glob("{}/*aarch64".format(os_list_dir))]
        os_list.extend(os_item for os_item in glob.glob("{}/*x86_64".format(os_list_dir)))
        return os_list

    @staticmethod
    def get_mindstudio_info():
        ms_list_dir = "{}/resources".format(ROOT_PATH)
        ms_list = [ms_item for ms_item in glob.glob("{}/MindStudio*/*aarch64".format(ms_list_dir))]
        ms_list.extend(ms_item for ms_item in glob.glob("{}/MindStudio*/*x86_64".format(ms_list_dir)))
        return ms_list

    def _delete_nexus_container(self):
        out, err = self._run_cmd("docker ps -a", ignore_errors=True)
        if "daemon running" in err:
            self._run_cmd("systemctl daemon-reload")
            self._run_cmd("systemctl restart docker")
            out, _ = self._run_cmd("docker ps -a")
        if "nexus" in out.split():
            self._run_cmd("docker rm -f nexus")
        self._run_cmd("docker network rm ip6net_nexus", ignore_errors=True)

    def _check_nexus_status(self):
        timeout = 0
        while True:
            time.sleep(1)
            timeout += 1
            out, _ = self._run_cmd("docker logs nexus", log=False)
            if "Nexus OSS" in out:
                break
            if timeout >= 300:
                raise RuntimeError("Nexus startup timeout")

    def _get_os_files(self, os_dir):
        files = []
        for file_name in os.listdir(os_dir):
            file_path = os.path.join(os_dir, file_name)
            if os.path.isdir(file_path):
                files.extend(self._get_os_files(file_path))
            else:
                files.append(file_path)
        return files

    def _create_data_dir(self):
        if os.path.exists(self.nexus_data_dir):
            try:
                shutil.rmtree(self.nexus_data_dir)
            except OSError:
                self._run_cmd("umount {}".format(self.nexus_data_dir))
                shutil.rmtree(self.nexus_data_dir)
        os.makedirs(self.nexus_data_dir, mode=0o700)
        self._run_cmd("mount -t tmpfs tmpfs {}".format(self.nexus_data_dir))

    def _run_nexus(self):
        self._delete_nexus_container()
        self._create_data_dir()
        network_command_opt = ""
        if self.working_on_ipv6:
            if not os.path.exists("/etc/docker/daemon.json"):
                os.makedirs("/etc/docker/", mode=0o755, exist_ok=True)
                with open("/etc/docker/daemon.json", "w") as fid:
                    json.dump({}, fid, indent=1)
            with open("/etc/docker/daemon.json") as fid:
                docker_settings = json.load(fid)
            docker_settings["experimental"] = True
            docker_settings["ip6tables"] = True
            with open("/etc/docker/daemon.json", "w") as fid:
                json.dump(docker_settings, fid, indent=1)
            self._run_cmd("systemctl daemon-reload")
            self._run_cmd("systemctl restart docker")
            self._run_cmd("docker network create --ipv6 --subnet 2001:0DB8::/112 ip6net_nexus")
            network_command_opt = "--network ip6net_nexus"
        self._run_cmd("docker load -i {}".format(self.nexus_image))
        start_nexus_cmd = "docker run -d --privileged --name nexus {} -p {}:8081 -v {}:/nexus-data {}".format(
            network_command_opt, self.nexus_run_port, self.nexus_data_dir, self.nexus_image_name
        )
        self._run_cmd(start_nexus_cmd)


class YumRepository(OsRepository):
    def create_blob(self):
        url = "{}/service/rest/v1/blobstores/file".format(self.nexus_url)
        data = {"softQuota": None, "path": "/nexus-data/blobs/yum", "name": "yum"}
        self._run_request(url, data=json.dumps(data).encode("utf-8"), headers=self.post_headers, method="POST")

    def create_repository(self):
        url = "{}/service/rest/v1/repositories/yum/hosted".format(self.nexus_url)
        os_info = self.get_download_os_info()
        for i in os_info:
            repository_name = os.path.basename(i)
            if repository_name in self.config_content["rpm_os"]:
                data = {
                    "name": repository_name,
                    "online": True,
                    "storage": {
                        "blobStoreName": "yum",
                        "strictContentTypeValidation": True,
                        "writePolicy": "ALLOW",
                    },
                    "cleanup": None,
                    "component": {
                        "proprietaryComponents": False,
                    },
                    "yum": {"repodataDepth": 0, "deployPolicy": "STRICT"},
                }
                self._run_request(url, data=json.dumps(data).encode("utf-8"), headers=self.post_headers, method="POST")

    def upload_rpm(self):
        base_url = "{}/repository/".format(self.nexus_url)
        download_os_list = self.get_download_os_info()
        for download_os in download_os_list:
            os_name = os.path.basename(download_os)
            if os_name not in self.config_content["rpm_os"]:
                continue
            os_deps = self._get_os_files(download_os)
            for os_dep in os_deps:
                with open(os_dep, "rb") as f:
                    file_content = f.read()
                url = urljoin(base_url, "{}/{}".format(os.path.basename(download_os), os.path.basename(os_dep)))
                self._run_request(url, data=file_content, headers=self.upload_headers, method="PUT")


class AptRepository(OsRepository):
    def generate_gpg_key(self):
        gpg_dir = os.path.expanduser("~/.gnupg")
        if os.path.exists(gpg_dir):
            shutil.rmtree(gpg_dir)
        base_cmd = "gpg --gen-key --batch"
        gpg_data = """Key-Type: RSA
        Key-Length: 3072
        Name-Real: nexus
        Expire-Date: 3d
        Passphrase: {}
        """.format(
            self.gpg_passwd
        )
        result = subprocess.Popen(
            shlex.split(base_cmd),
            shell=False,
            universal_newlines=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        result.communicate(input=gpg_data)
        if result.returncode != 0:
            raise RuntimeError("GPG key generation failed")

    def export_gpg_key(self):
        gpg_key_dir = os.path.dirname(self.nexus_image)
        gpg_pub_key = "{}/nexus_pub.asc".format(gpg_key_dir)
        gpg_pri_key = "{}/nexus_pri.asc".format(gpg_key_dir)
        if os.path.exists(gpg_pub_key):
            os.unlink(gpg_pub_key)
        if os.path.exists(gpg_pri_key):
            os.unlink(gpg_pri_key)
        export_public_key_cmd = "gpg -a -o {} --export nexus".format(gpg_pub_key)
        export_private_key_cmd = (
            "gpg --batch --pinentry-mode=loopback --yes --passphrase {} "
            "-a -o {} --export-secret-key nexus".format(self.gpg_passwd, gpg_pri_key)
        )
        centos_release = "/etc/centos-release"
        if os.path.exists(centos_release):
            export_private_key_cmd = "gpg -a -o {} --export-secret-key nexus".format(gpg_pri_key)
        self._run_cmd(export_public_key_cmd)
        self._run_cmd(export_private_key_cmd, log=False)
        with open(gpg_pri_key, "r") as f:
            gpg_pri_content = f.read()
        return gpg_pri_content

    def create_blob(self):
        url = "{}/service/rest/v1/blobstores/file".format(self.nexus_url)
        data = {"softQuota": None, "path": "/nexus-data/blobs/apt", "name": "apt"}
        self._run_request(url, data=json.dumps(data).encode("utf-8"), headers=self.post_headers, method="POST")

    def create_repository(self, keypair):
        url = "{}/service/rest/v1/repositories/apt/hosted".format(self.nexus_url)
        os_info = self.get_download_os_info()
        for i in os_info:
            repository_name = os.path.basename(i)
            if repository_name in self.config_content["deb_os"]:
                codename = self.config_content["codename"][repository_name]
                data = {
                    "name": repository_name,
                    "online": True,
                    "storage": {
                        "blobStoreName": "apt",
                        "strictContentTypeValidation": True,
                        "writePolicy": "ALLOW",
                    },
                    "cleanup": None,
                    "component": {
                        "proprietaryComponents": False,
                    },
                    "apt": {"distribution": codename},
                    "aptSigning": {"keypair": keypair, "passphrase": self.gpg_passwd},
                }
                self._run_request(url, data=json.dumps(data).encode("utf-8"), headers=self.post_headers, method="POST")

    def upload_deb(self):
        base_url = "{}/repository/".format(self.nexus_url)
        download_os_list = self.get_download_os_info()
        ms_list = self.get_mindstudio_info()
        if ms_list:
            download_os_list.extend(ms_list)
        for download_os in download_os_list:
            if os.path.basename(download_os) not in self.config_content["deb_os"]:
                continue
            os_deps = self._get_os_files(download_os)
            for os_dep in os_deps:
                with open(os_dep, "rb") as f:
                    file_content = f.read()
                url = urljoin(base_url, "{}/".format(os.path.basename(download_os)))
                self._run_request(url, data=file_content, headers=self.upload_headers, method="POST")


def main(ip=None, port=58081):
    yum_repository = YumRepository(ip, port)
    download_os_list = [os.path.basename(os_name) for os_name in yum_repository.get_download_os_info()]
    have_rpm = any(os_item in yum_repository.config_content["rpm_os"] for os_item in download_os_list)
    have_deb = any(os_item in yum_repository.config_content["deb_os"] for os_item in download_os_list)
    yum_repository.init_nexus()
    if have_rpm:
        yum_repository.create_blob()
        yum_repository.create_repository()
        yum_repository.upload_rpm()
    if have_deb:
        apt_repository = AptRepository(ip, port)
        apt_repository.create_blob()
        apt_repository.generate_gpg_key()
        gpg_pair_key = apt_repository.export_gpg_key()
        if gpg_pair_key == "":
            raise RuntimeError("The file content is empty")
        apt_repository.create_repository(gpg_pair_key)
        apt_repository.upload_deb()


if __name__ == "__main__":
    main()
