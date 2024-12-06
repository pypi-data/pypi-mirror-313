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
import sys
import argparse
import logging
import logging.config
from functools import wraps

import utils

__cached__ = 'ignore'  # fix bug for site.py in ubuntu_18.04_aarch64

LOG = logging.getLogger('ascend_deployer')
LOG_OP = logging.getLogger('install_operation')


def add_log(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        cmd = ' '.join(sys.argv[1:])
        dl_scene = False
        if 'dl' in cmd:  # only for support XX ugly implementation
            dl_scene = True
        reason = ''
        try:
            f(*args, **kwargs)
            if dl_scene:
                LOG.info("[INFO] Ascend DL deployed success --ascend-deployer")
            return 0
        except SystemExit as e:
            if e.code == 0:
                return 0
            reason = 'exit code: {}'.format(e.code)
            return -1
        except KeyboardInterrupt:  # handle KeyboardInterrupt
            reason = "User interrupted the program by Keyboard"
            return -1
        except BaseException as e:  # handle other exceptions
            LOG.exception(e)
            reason = str(e)
            return -1
        finally:
            msg = "run cmd: {} successfully".format(cmd)
            if reason:
                msg = "run cmd: {} failed, reason: {}".format(cmd, reason)
            print(msg)
            if dl_scene and reason:
                LOG.error("[ERROR]Ascend DL deployed failed --ascend-deployer")
            if reason:
                LOG_OP.error(msg)
            else:
                LOG_OP.info(msg)

    return wrap


class CLI(object):
    def __init__(self, prog, desc, epilog=None):
        self.parser = argparse.ArgumentParser(
            prog=prog, description=desc, epilog=epilog, formatter_class=utils.HelpFormatter)
        self.parser.add_argument("--check", dest="check", action="store_true", default=False, help="check environment")
        self.parser.add_argument("--clean", dest="clean", action="store_true", default=False,
                                 help="clean resources on remote servers")
        self.parser.add_argument("--force_upgrade_npu", dest="force_upgrade_npu", action="store_true", default=False,
                                 help="can force upgrade NPU when not all devices have exception")
        self.parser.add_argument("--verbose", dest="verbose", action="store_true", default=False, help="Print verbose")
        self.parser.add_argument("--install", dest="install", nargs="+", choices=utils.install_items,
                                 action=utils.ValidChoices,
                                 metavar="<package_name>", help="Install specific package: %(choices)s")
        self.parser.add_argument("--stdout_callback", dest="stdout_callback",
                                 help="set display plugin, e.g. ansible_log")
        self.parser.add_argument("--install-scene", dest="scene", nargs="?", choices=utils.scene_items,
                                 metavar="<scene_name>", help="Install specific scene: %(choices)s")
        self.parser.add_argument("--patch", dest="patch", nargs="+", choices=utils.patch_items,
                                 action=utils.ValidChoices,
                                 metavar="<package_name>", help="Patching specific package: %(choices)s")
        self.parser.add_argument("--patch-rollback", dest="patch_rollback", nargs="+", choices=utils.patch_items,
                                 action=utils.ValidChoices,
                                 metavar="<package_name>", help="Rollback specific package: %(choices)s")
        self.parser.add_argument("--test", dest="test", nargs="+", choices=utils.test_items, metavar="<target>",
                                 action=utils.ValidChoices,
                                 help="test the functions: %(choices)s")
        self.parser.add_argument("--hccn", dest="hccn", action="store_true", default=False,
                                 help="Setting hccn")
        exclusive_group = self.parser.add_mutually_exclusive_group()
        exclusive_group.add_argument("--nocopy", dest="no_copy", action="store_true", default=False,
                                     help="do not copy resources to remote servers when install for remote")
        exclusive_group.add_argument("--only_copy", dest="only_copy", action="store_true", default=False,
                                     help="copy the packages of the software you choose to install, but do not install."
                                          "only existing packages will be copied. If the package does not exist,"
                                          "please check and download it.")
        self.parser.add_argument("--skip_check", dest="skip_check", action="store_true", default=False,
                                 help="Control whether to perform a pre-installation check")

    @add_log
    def run(self):
        args = self.parser.parse_args(utils.args_with_comma(sys.argv[1:]))
        if not any([args.install, args.scene, args.patch, args.patch_rollback, args.test, args.check, args.clean,
                    args.hccn]):
            self.parser.print_help()
            raise Exception("expected one valid argument at least")
        if args.install and args.scene:
            raise Exception("Unsupported --install and --install-scene at same time")

        if args.stdout_callback:
            os.environ['ANSIBLE_STDOUT_CALLBACK'] = args.stdout_callback
        os.environ['ANSIBLE_CACHE_PLUGIN_CONNECTION'] = os.path.join(utils.ROOT_PATH, 'facts_cache')
        os.environ['ANSIBLE_CONFIG'] = os.path.join(utils.ROOT_PATH, 'ansible.cfg')
        os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning'

        import jobs
        if any([args.install, args.scene, args.patch]) and not args.check:
            if not jobs.accept_eula():
                LOG_OP.error('reject EULA, quit to install')
                raise Exception('reject EULA, quit to install')
            LOG_OP.info("accept EULA, start to install")
        if args.scene == 'auto':
            print('Warning: --install-scene=auto feature will soon be deprecated.')
        jobs.PrepareJob().run()
        ansible_args = ['-vv'] if args.verbose else []
        check_tags = args.install if args.install else []
        if args.scene:
            if args.scene == "mindspore":
                check_tags.append("mindspore_scene")
            else:
                check_tags.append(args.scene)

        ip = jobs.get_localhost_ip()
        envs = {
            'force_upgrade_npu': 'true' if args.force_upgrade_npu else 'false',
            'do_upgrade': 'true',
            'working_on_ipv6': 'true' if ':' in ip else 'false',
            'use_k8s_version': os.environ.get('USE_K8S_VERSION', '1.25.3'),
        }
        if args.check:
            if not check_tags:
                self.parser.print_usage()
                raise Exception("The check option must be used together with either install or install-scene, for "
                                "example: '--install=<package_name> --check' or '--install-scene=<scene_name> --check'")
            total_tags = []
            for tmp_tags in (args.install, args.scene, args.patch, args.patch_rollback):
                if not tmp_tags:
                    continue
                if isinstance(tmp_tags, str):
                    total_tags.append(tmp_tags)
                if isinstance(tmp_tags, list):
                    total_tags.extend(tmp_tags)

            envs['hosts_name'] = utils.get_hosts_name(total_tags)
            return jobs.process_check(check_tags, no_copy=True, envs=envs, ansible_args=ansible_args)

        for handler, tags in (
                (jobs.process_install, args.install),
                (jobs.process_scene, args.scene),
                (jobs.process_patch, args.patch),
                (jobs.process_patch_rollback, args.patch_rollback)):
            if not tags:
                continue
            ip = jobs.get_localhost_ip()
            job = jobs.ResourcePkg(tags, "copy_pkgs" in tags)
            nexus_url = job.start_nexus_daemon(ip)
            if not args.no_copy:
                job.handle_pkgs()
            envs['hosts_name'] = utils.get_hosts_name(tags)
            if nexus_url:
                envs['nexus_url'] = nexus_url
            if not args.skip_check and tags:
                jobs.process_check(tags, no_copy=True, envs=envs, ansible_args=ansible_args)
            result = handler(tags, no_copy=args.no_copy, only_copy=args.only_copy, envs=envs, ansible_args=ansible_args)
            job.clean(ip)
            return result
        if args.test:
            envs = {'hosts_name': 'worker'}
            os.environ['ANSIBLE_STDOUT_CALLBACK'] = 'ansible_log'
            if '-v' not in ansible_args:  # test always detail output
                ansible_args.append('-v')
            return jobs.process_test(args.test, envs=envs, ansible_args=ansible_args)
        if args.clean:
            run_args = ['worker', '-m', 'shell', '-a', 'rm -rf ~/resources*.tar ~/resources']
            run_args.extend(ansible_args)
            return jobs.process_clean(run_args)
        if args.hccn:
            if not args.skip_check:
                jobs.process_hccn_check(['hccn'], no_copy=True, envs=envs, ansible_args=ansible_args)
            return jobs.process_hccn(None, ansible_args=ansible_args)


def main():
    os.umask(0o022)
    logging.config.dictConfig(utils.LOGGING_CONFIG)
    cli = CLI(
        "ascend-deployer",
        "Manage Ascend Packages and dependence packages for specified OS"
    )
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
