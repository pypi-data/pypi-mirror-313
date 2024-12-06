#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Huawei Technologies Co., Ltd
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
"""downloader"""
import glob
import os
import sys
import time
from io import StringIO
from typing import List

from . import deb_downloader
from . import download_util
from . import logger_config
from . import os_dep_downloader
from . import pip_downloader
from . import rpm_downloader
from . import other_downloader
from . import dl_dependency_downloader
from .download_data import DownloadData
from .download_util import State, Color, get_free_space_b, CONFIG_INST, DOWNLOAD_INST
from .parallel_file_downloader import ParallelDownloader, DownloadFileInfo

FILE_PATH = os.path.realpath(__file__)
CUR_DIR = os.path.dirname(__file__)

LOG = logger_config.LOG
LOG_OPERATION = logger_config.LOG_OPERATION
MAX_DOWNLOAD_SIZE = 20 * (2 ** 30)


class MockPrinter:
    def __init__(self, lines, max_lines=3):
        self.max_lines = max_lines
        self.lines = lines

    def clear_last_lines(self, lines):
        for _ in range(lines):
            sys.stdout.write('\x1b[F\x1b[2K')

    def mock_print(self, *args, sep=' ', end='\n', file=None, max_length=100):
        line = sep.join(map(str, args)) + end
        if len(line) > max_length:
            line = line[:max_length - 3] + "..." + end

        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

        self.lines.append(line)

        for line in self.lines:
            sys.stdout.write(line)
        sys.stdout.flush()


class DependencyDownload(object):
    def __init__(self, os_list, software_list, download_path, check):
        self.os_list = os_list
        self.dst = download_util.get_download_path()
        self.download_data = DownloadData(os_list, software_list, dst=self.dst)
        self.software_mgr = self.download_data.software_mgr
        self.origin_download = None
        self.origin_cann_download = None
        self.progress = 0
        self.download_items = []
        self.res_dir = os.path.join(self.dst, "resources")
        self.finished_items = []
        self.extra_schedule = None
        self.origin_check_hash = None
        self.origin_print = print
        self.download_path = download_path
        self.lines = []
        if check and software_list:
            self.check_software_list(os_list, software_list)
        if os.name == 'nt':
            os.system('chcp 65001')
            os.system('cls')

    @staticmethod
    def check_space(download_path):
        free_size = get_free_space_b(download_path)
        if free_size < MAX_DOWNLOAD_SIZE:
            print(Color.warn("[WARN] the disk space of {} is less than {:.2f}GB".format(download_path,
                                                                                        MAX_DOWNLOAD_SIZE / (
                                                                                                1024 ** 3))))

    def check_software_list(self, os_list, software_list):
        """
        check the download software list
        :param os_list: download os list
        :param software_list: download software list
        注:版本配套信息影响Smartkit界面展示，请勿随意修改
        """
        check_stat, msg = self.software_mgr.check_selected_software(os_list, software_list)
        if check_stat == State.EXIT:
            print("[ERROR] {}".format(msg))
            LOG.error("[ERROR] {}".format(msg))
            sys.exit(1)
        if check_stat == State.ASK:
            if CONFIG_INST.is_skip_confirm():
                LOG.info("Skip download confirmation, Versions do not match, force download.")
                return
            print("[ASCEND][WARNING]: {} please check it.".format(msg[0].upper() + msg[1:]))
            while True:
                answer = input("need to force download or not?(y/n)")
                if answer in {'y', 'yes'}:
                    print("Versions do not match, force download.")
                    LOG.info("Versions do not match, force download.")
                    break
                elif answer in {'n', 'no'}:
                    print("Versions do not match, exit.")
                    LOG.info("Versions do not match, exit.")
                    sys.exit(0)
                else:
                    print("Invalid input, please re-enter!")

    @staticmethod
    def download_python_packages(os_list, res_dir):
        """
        download_python_packages
        """
        return pip_downloader.download(os_list, res_dir)

    def download_os_packages(self, os_list, software_list, dst):
        """
        download_os_packages
        """
        os_dep = os_dep_downloader.OsDepDownloader(self.download_data)
        return os_dep.download(os_list, software_list, dst)

    def mock_print(self, *args, **kwargs):
        printer = MockPrinter(self.lines)
        printer.mock_print(*args, **kwargs)
        printer.clear_last_lines(len(self.lines))

    def mock_download(self, url: str, dst_file_name: str, sha256=""):
        # mock other_downloader.DOWNLOAD_INST.download
        if dst_file_name.endswith(".xml") or dst_file_name.endswith("sqlite.bz2") or dst_file_name.endswith(
                "sqlite.xz") or dst_file_name.endswith("sqlite.gz"):
            return self.origin_download(url, dst_file_name, sha256)
        if not sha256 and 'sha256=' in url:
            sha256 = url.rsplit('sha256=')[-1]
        self.download_items.append(
            DownloadFileInfo(url=url, dst_file_path=dst_file_name, filename=os.path.basename(dst_file_name),
                             sha256=sha256))
        return True

    def mock_check_hash(self, *args, **kwargs):
        return True

    # 通过关闭实际下载，mock实际下载函数和哈希比较函数，收集下载信息
    def collect_python_and_os_pkgs_info(self, os_list, software_list, download_path) -> List[DownloadFileInfo]:
        self.check_space(self.download_path)
        msg = Color.info('start analyzing the amount of packages to be downloaded ...')
        self.origin_print(msg)
        LOG.info(msg, extra=logger_config.LOG_CONF.EXTRA)
        self.origin_download = DOWNLOAD_INST.download
        DOWNLOAD_INST.download = self.mock_download
        self.origin_check_hash = download_util.CH.check_hash
        download_util.CH.check_hash = self.mock_check_hash
        pip_downloader.print = self.mock_print
        download_util.print = self.mock_print
        os_dep_downloader.print = self.mock_print
        deb_downloader.print = self.mock_print
        rpm_downloader.print = self.mock_print
        try:
            self.download_python_and_os_pkgs(os_list, software_list, download_path)
        except Exception as e:
            raise e
        finally:
            print = self.origin_print
            download_util.CH.check_hash = self.origin_check_hash
            DOWNLOAD_INST.download = self.origin_download
        msg = f'python_and_os_pkgs finish analyzing ...'
        print(msg)
        LOG.info(msg, extra=logger_config.LOG_CONF.EXTRA)
        return self.download_items

    def download_python_and_os_pkgs(self, os_list, software_list, dst):
        """
        download all resources
        """
        res_dir = os.path.join(dst, "resources")
        self.download_python_packages(os_list, res_dir)
        if not software_list:
            software_list = []
        self.download_os_packages(os_list, software_list, res_dir)

    def collect_other_download_info(self) -> List[DownloadFileInfo]:
        download_file_list = []

        other_downloader.print = self.mock_print
        od = other_downloader.OtherDownloader(self.download_data)
        download_file_list.extend(od.collect_specified_python())
        download_file_list.extend(od.collect_other_software())
        download_file_list.extend(od.collect_other_pkgs())
        download_file_list.extend(od.collect_ai_framework())

        if od.warning_message:
            print("\n".join(od.warning_message))

        dl_dependency_downloader.print = self.mock_print
        dl_mef_downloader = dl_dependency_downloader.DlComponentDownloader(self.download_data)
        download_file_list.extend(dl_mef_downloader.collect_dl_contents_dependency())
        msg = f'other_download finish analyzing ...'
        print(msg)
        LOG.info(msg, extra=logger_config.LOG_CONF.EXTRA)
        return download_file_list

    @staticmethod
    def parallel_download_pkgs(download_file_list: List[DownloadFileInfo]):
        ParallelDownloader(download_file_list, CONFIG_INST.is_parallel_download()).start_download()


def delete_glibc(os_list, download_path):
    delete_os_list = ['Kylin_V10Tercel_aarch64', 'Kylin_V10Tercel_x86_64']
    for i in delete_os_list:
        if i in os_list:
            os_dir = os.path.join(download_path, 'resources', i)
            glibc = glob.glob('{}/glibc-[0-9]*'.format(os_dir))
            try:
                os.unlink(glibc[0])
            except IndexError:
                pass


def download_dependency(os_list, software_list, download_path, check):
    download_status = "Failed"
    err_log = ""
    software_list = software_list or []
    start_time = time.time()
    try:
        download_util.check_base()
        dependency_download = DependencyDownload(os_list, software_list, download_path, check)
        download_file_list = []
        download_file_list += dependency_download.collect_python_and_os_pkgs_info(os_list, software_list, download_path)
        download_file_list += dependency_download.collect_other_download_info()
        dependency_download.parallel_download_pkgs(download_file_list)
    except (KeyboardInterrupt, SystemExit):
        download_status = "Failed"
        err_log = Color.error("download failed,keyboard interrupt or system exit,please check.")
    except download_util.DownloadError as e:
        download_status = "Failed"
        err_log = Color.error("download failed, download from {} to {} failed, {}".format(e.url, e.dst_file, e.err_msg))
    except download_util.DownloadCheckError as e:
        download_status = "Failed"
        err_log = Color.error("{} download verification failed".format(e.dst_file))
    except download_util.PythonVersionError as e:
        download_status = "Failed"
        err_log = Color.error("download failed, {}, please check.".format(e.err_msg))
    except Exception as e:
        download_status = "Failed"
        err_log = Color.error("download failed with error {}, please retry.".format(e))
    else:
        download_status = "Success"
        err_log = ""
    finally:
        if software_list:
            download_result = "\ndownload and check --os-list={} --download={}:{}".format(",".join(os_list),
                                                                                          ",".join(software_list),
                                                                                          download_status)
        else:
            download_result = "\ndownload and check --os-list={}:{}".format(",".join(os_list), download_status)
        if download_status == "Success":
            log_msg = "\n" + err_log + download_result
        else:
            log_msg = "\n\n" + err_log + download_result
        print(log_msg)
        print("Time Cost:", "{:.2f}s".format(time.time() - start_time))
        LOG_OPERATION.info(log_msg, extra=logger_config.LOG_CONF.EXTRA)
        delete_glibc(os_list, download_path)
