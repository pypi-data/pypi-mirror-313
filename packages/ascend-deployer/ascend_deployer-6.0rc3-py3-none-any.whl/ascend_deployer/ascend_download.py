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
import sys
sys.path.append('.')
import argparse
import utils
from downloader.downloader import download_dependency
from downloader.download_util import get_download_path


class CLI(object):
    def __init__(self, prog, desc, epilog):
        self.parser = argparse.ArgumentParser(
            prog=prog, formatter_class=utils.HelpFormatter, description=desc, epilog=epilog)
        self.parser.add_argument(
            "--os-list", dest="os_list", nargs="+", required=True, choices=utils.os_items, action=utils.ValidChoices,
            metavar="<OS>", help="Specific OS list to download, supported os are: %(choices)s")
        self.parser.add_argument(
            "--download", dest="pkg_list", nargs="+", required=False, choices=utils.pkg_items,
            action=utils.ValidChoices, default=[],
            metavar="<PKG>|<PKG>==<Version>", help="Specific package list to download, supported packages: %(choices)s")

    def run(self, args, check):
        if not args:
            args = sys.argv[1:]
        args = self.parser.parse_args(utils.args_with_comma(args))
        download_dependency(args.os_list, args.pkg_list, get_download_path(), check)


def main(args=None, check=True):
    cli = CLI(
        "ascend-download",
        "Download Ascend Packages and dependence packages for specified OS",
        "notes: When <Version> is missing, <PKG> is the latest."
    )
    return cli.run(args, check)


if __name__ == '__main__':
    sys.exit(main())
