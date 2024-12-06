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
import obs

try:
    from urllib.parse import unquote, urlparse
    from urllib.request import getproxies
except ImportError:
    from urlparse import urlparse
    from urllib import unquote, getproxies

PART_SIZE = 10 * 1024 * 1024
OBS_HOST = "https://obs.cn-east-2.myhuaweicloud.com"
OBS_BUCKET = "ascend-repo"
OBS_URL_STARTING = "https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/"


class ProxyInfo:
    def __init__(self, username, password, hostname, port):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port


def get_http_proxy_from_env():
    proxies = getproxies()
    https_proxy = proxies.get("https", "")
    if not https_proxy:
        raise ValueError("no proxy setting found, access directly")
    proxy = urlparse(https_proxy)
    password = (
        proxy.password if proxy.password is None else unquote(proxy.password, "utf-8")
    )
    proxy_info = ProxyInfo(proxy.username, password, proxy.hostname, proxy.port)
    return proxy_info


def obs_urlretrieve(url, local_file_path, progress_updater=None):
    try:
        proxy_info = get_http_proxy_from_env()
        user, password, host, port = proxy_info.username, proxy_info.password, proxy_info.hostname, proxy_info.port
    except ValueError:
        user, password, host, port = None, None, None, None
    obs_client = obs.ObsClient(
        server=OBS_HOST,
        proxy_host=host,
        proxy_port=port,
        proxy_username=user,
        proxy_password=password,
        max_retry_count=1,
    )
    object_key = unquote(url.replace(OBS_URL_STARTING, ""), "utf-8")
    try:
        resp = obs_client.downloadFile(
            OBS_BUCKET,
            object_key,
            downloadFile=local_file_path,
            partSize=PART_SIZE,
            taskNum=1,
            enableCheckpoint=True,
            progressCallback=progress_updater,
        )
        if resp.status < 300:
            return local_file_path, ""
        else:
            raise RuntimeError("failed in downloading")
    except Exception as e:
        raise e
    finally:
        obs_client.close()
