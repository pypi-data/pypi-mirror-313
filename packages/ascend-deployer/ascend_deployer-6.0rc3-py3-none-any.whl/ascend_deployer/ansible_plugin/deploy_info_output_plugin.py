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
import datetime
import json
import os.path
import re
import sys
import threading
import time
import traceback

import ansible.plugins.callback
import yaml

try:
    # 适配python2 json打印中文异常问题
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_CONFIG_PATH = os.path.join(CUR_DIR, "progress_config.json")
ROOT_DIR = os.path.dirname(CUR_DIR)
PLAYBOOK_DIR = os.path.join(ROOT_DIR, "playbooks")
PROCESS_DIR = os.path.join(ROOT_DIR, "playbooks", "process")
HOME_PATH = os.path.expanduser('~')
DEPLOY_INFO_OUTPUT_DIR = os.path.join(HOME_PATH, ".ascend_deployer", "deploy_info")

ERROR_MSG_LIST = []


def error_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exc_info = traceback.format_exc()
            ERROR_MSG_LIST.append("Exception: {}, Traceback: {}".format(str(e), str(exc_info)))
            raise e

    return wrapper


TIME_FORMAT_PATTERN = "%Y-%m-%d %H:%M:%S"


def time_format(time_stamp):
    if not time_stamp:
        return ""
    return datetime.datetime.fromtimestamp(time_stamp).strftime(TIME_FORMAT_PATTERN)


class ProgressConfig:

    def __init__(self, name="", duration=60, primary_plays=None, desc_en="", desc_zh="", *args, **kwargs):
        self.name = name
        self.duration = duration
        self.desc_en = desc_en
        self.desc_zh = desc_zh
        self.primary_plays = primary_plays or []


PREPARE_CONFIG = ProgressConfig(name="prepare", desc_en="Prepare", desc_zh="准备阶段")


@error_catcher
def load_progress_configs():
    with open(PROGRESS_CONFIG_PATH) as fs:
        config_json_list = json.load(fs) or []
        return [ProgressConfig(**config_json) for config_json in config_json_list]


CONFIGS = [PREPARE_CONFIG] + load_progress_configs()


class DeployStatus(object):
    DEPLOY_STATUS = "deploy_status"

    WAIT = "wait"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    SKIP = "skip"


DEPLOY_FINISH_STATUS = (DeployStatus.FAILED, DeployStatus.SKIP, DeployStatus.SUCCESS)


class HostStatus(object):
    WAIT = "wait"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    UNREACHABLE = "unreachable"


HOST_FINISH_STATUS = (HostStatus.FAILED, HostStatus.UNREACHABLE, HostStatus.SUCCESS)


class HostDeployInfo:

    def __init__(self, ip):
        self.ip = ip
        self.status = HostStatus.DEPLOYING
        self.msg_list = []

    def to_json(self):
        return {
            "ip": self.ip,
            "status": self.status,
            "msg_list": self.msg_list
        }


class PlaybookProgressOutput(object):

    def __init__(self, name="", progress=0.0, expected_duration=0.0, actual_duration=0.0, deploy_status="",
                 start_time="", end_time="", host_info=None, deploy_info=None, desc_en="", desc_zh=""):
        self.name = name
        self.progress = progress
        self.expected_duration = expected_duration
        self.actual_duration = actual_duration
        self.deploy_status = deploy_status
        self.start_time = start_time
        self.end_time = end_time
        self.host_info = host_info
        self.deploy_info = deploy_info or []
        self.desc_en = desc_en
        self.desc_zh = desc_zh

    def to_json(self):
        return {
            "name": self.name,
            "progress": self.progress,
            "expected_duration": self.expected_duration,
            "actual_duration": self.actual_duration,
            "deploy_status": self.deploy_status,
            "deploy_info": self.deploy_info,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "host_info_list": self.host_info,
            "desc_en": self.desc_en,
            "desc_zh": self.desc_zh,
        }


class DeployerProgressOutput(object):

    def __init__(self, cur_playbook=None, playbooks=None, total_host_info=None, deploy_status="", error_msg=""):
        self.cur_playbook = cur_playbook or ""
        self.playbooks = playbooks or []
        self.total_host_info = total_host_info or []
        self.total_actual_duration = round(sum(playbook.actual_duration for playbook in self.playbooks), 2)
        self.total_expected_duration = round(sum(playbook.expected_duration for playbook in self.playbooks), 2)
        self.deploy_status = deploy_status
        self.error_msg = error_msg

    @property
    def progress(self):
        if self.deploy_status == DeployStatus.SUCCESS:
            return 1.0
        progress_sum = sum(playbook.expected_duration * playbook.progress for playbook in self.playbooks)
        total_progress = 0 if self.total_expected_duration == 0 else (progress_sum / self.total_expected_duration)
        total_progress = round(total_progress, 2)
        return 0.99 if total_progress >= 0.99 else total_progress

    def to_json(self):
        return {
            "deploy_status": self.deploy_status,
            "progress": self.progress,
            "cur_playbook": self.cur_playbook,
            "playbooks": [playbook.to_json() for playbook in self.playbooks],
            "total_host_info": self.total_host_info,
            "total_actual_duration": self.total_actual_duration,
            "total_expected_duration": self.total_expected_duration,
            "error_msg": self.error_msg
        }


class InstallHandler(object):
    _TIME_INCREASE_RATIO_PER_SERVER = 0.01

    def __init__(self, progress_config):
        self.progress_config = progress_config
        self.deploy_status = DeployStatus.WAIT
        self.start_time = None
        self.end_time = None
        self.host_num = 1
        self.host_info_dict = {}
        self.deploy_info_list = []

    @property
    def actual_duration(self):
        if not self.start_time:
            return 0
        end_time = self.end_time if self.end_time else time.time()
        return round(end_time - self.start_time, 2)

    @property
    def expected_duration(self):
        duration_ratio = 1 + (self.host_num - 1) * self._TIME_INCREASE_RATIO_PER_SERVER
        return round(float(self.progress_config.duration) * duration_ratio, 2)

    @property
    def progress(self):
        if self.deploy_status in (DeployStatus.SUCCESS, DeployStatus.SKIP):
            return 1.0
        if not self.start_time:
            return 0.0
        actual_duration = self.actual_duration
        expected_duration = self.expected_duration
        progress = round(actual_duration / expected_duration, 2)
        return 0.99 if progress >= 0.99 else progress

    def add_msg(self, msg, host=None):
        if host:
            host_task_info = self.host_info_dict.setdefault(host, HostDeployInfo(host))
            host_task_info.msg_list.append(msg)
        else:
            self.deploy_info_list.append(msg)

    def handle_deploy_status(self, status):
        if self.deploy_status in DEPLOY_FINISH_STATUS:
            return
        self.deploy_status = status

    def handle_host_status(self, host, status=HostStatus.DEPLOYING):
        host_task_info = self.host_info_dict.setdefault(host, HostDeployInfo(host))
        if host_task_info.status in HOST_FINISH_STATUS:
            return
        host_task_info.status = status

    def set_status_after_deploy(self, status=HostStatus.SUCCESS):
        for host in self.host_info_dict.keys():
            self.handle_host_status(host, status)

    def on_play_start(self, play_name, host_num=1):
        self.add_msg("Play[{}] start.".format(play_name))
        if not self.start_time:
            self.start_time = time.time()
            self.host_num = host_num
            self.handle_deploy_status(DeployStatus.DEPLOYING)

    def on_handler_end(self):
        self.end_time = time.time()
        self.handle_deploy_status(DeployStatus.SUCCESS)
        self.set_status_after_deploy(HostStatus.SUCCESS)

    def is_play_in_handler(self, play_name):
        return play_name in self.progress_config.primary_plays

    def on_task_start(self, task_name):
        self.add_msg("Task[{}] start.".format(task_name))

    def on_task_end(self, host, task_name, deploy_status, task_status, deploy_info):
        self.handle_deploy_status(deploy_status)
        self.handle_host_status(host, DeployStatus.DEPLOYING)
        self.add_msg("Task[{}] {}.{}".format(task_name, task_status, (" " + deploy_info) or ""), host)

    def on_task_failed(self, host, task_name, failed_info):
        self.handle_deploy_status(DeployStatus.FAILED)
        self.handle_host_status(host, HostStatus.FAILED)
        self.on_task_end(host, task_name, DeployStatus.FAILED, DeployStatus.FAILED, failed_info)

    def on_unreachable(self, host):
        self.handle_deploy_status(DeployStatus.FAILED)
        self.handle_host_status(host, HostStatus.UNREACHABLE)
        self.add_msg("Host[{}] is unreachable.".format(host), host)

    def to_host_info_list(self):
        return [host_info.to_json() for host_info in self.host_info_dict.values()]

    @error_catcher
    def get_playbook_output(self):
        return PlaybookProgressOutput(
            name=self.progress_config.name,
            progress=self.progress,
            deploy_info=self.deploy_info_list,
            deploy_status=self.deploy_status,
            expected_duration=self.expected_duration,
            actual_duration=self.actual_duration,
            start_time=time_format(self.start_time),
            host_info=self.to_host_info_list(),
            end_time=time_format(self.end_time),
            desc_zh=self.progress_config.desc_zh,
            desc_en=self.progress_config.desc_en
        )


class InstallParser(object):
    PROCESS_INSTALL_YML = os.path.join(PROCESS_DIR, "process_install.yml")
    PROCESS_SCENE_YML = os.path.join(PROCESS_DIR, "process_scene.yml")
    PROCESS_HCCN_YML = os.path.join(PROCESS_DIR, "process_hccn.yml")
    SCENE_DIR = os.path.join(PLAYBOOK_DIR, "scene")
    PLAYBOOK_NAME_KEY = "playbook_name"

    PROCESS_TYPE_INSTALL = "install"
    PROCESS_TYPE_SCENE = "scene"
    PROCESS_TYPE_HCCN = "hccn"
    SUPPORTED_PROCESS_TYPES = (PROCESS_TYPE_INSTALL, PROCESS_TYPE_SCENE, PROCESS_TYPE_HCCN)

    @staticmethod
    def _load_yaml(file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as fs:
            return yaml.safe_load(fs)

    @classmethod
    def _add_playbook_name(cls, import_item):
        playbook_rpath = import_item.get("import_playbook", "")
        playbook_name = playbook_rpath.rsplit("/", 1)[-1]
        target_playbook = {cls.PLAYBOOK_NAME_KEY: playbook_name}
        target_playbook.update(import_item)
        return target_playbook

    @classmethod
    def _parse_playbook_info(cls, yml_path):
        """
         读取import playbook的yaml，保留原结构，补充playbook_name字段
         return 样例：
         [{
            "name": "install toolkit",
            "import_playbook": "../install/install_toolkit.yml",
            "playbook_name": "install_toolkit.yml"
         }]
        """
        import_playbook_infos = []
        import_item_list = cls._load_yaml(yml_path) or []
        for import_item in import_item_list:
            if not isinstance(import_item, dict):
                continue
            import_playbook_item = cls._add_playbook_name(import_item)
            import_playbook_infos.append(import_playbook_item)
        return import_playbook_infos

    @classmethod
    def _find_target_playbooks_by_tags(cls, process_yml_path, tags):
        """
        从process yaml中找到tags对应的playbook信息
         return 样例：
         [{
            "name": "install toolkit",
            "import_playbook": "../install/install_toolkit.yml",
            "playbook_name": "install_toolkit.yml"
         }]
        """
        tag_set = set(tags)
        target_playbooks = []
        for import_playbook_info in cls._parse_playbook_info(process_yml_path):
            yml_tags = import_playbook_info.get("tags", [])
            if "," in yml_tags:
                yml_tags = yml_tags.split(",")
            if isinstance(yml_tags, str) and yml_tags in tag_set:
                target_playbooks.append(import_playbook_info)
            elif isinstance(yml_tags, list) and (set(yml_tags) & tag_set):
                target_playbooks.append(import_playbook_info)
        return target_playbooks

    @classmethod
    def read_primary_plays(cls, playbook_rela_path):
        """
        从playbook里读play
        """
        playbook_path = os.path.join(PROCESS_DIR, playbook_rela_path)
        playbook_json = cls._load_yaml(playbook_path) or []
        return filter(bool, [play.get("name", "") for play in playbook_json])

    @classmethod
    def _map_install_progress_config(cls, install_playbook):
        """
        根据playbook名映射为对应的playbook config
        """
        if not install_playbook:
            return None
        install_playbook_basename = install_playbook.get(cls.PLAYBOOK_NAME_KEY, "") \
            .replace(".yml", "").replace(".yaml", "")
        for playbook_config in CONFIGS:
            if install_playbook_basename == playbook_config.name:
                playbook_config.primary_plays.extend(cls.read_primary_plays(install_playbook.get("import_playbook")))
                return playbook_config
        return None

    @classmethod
    def _install_playbooks_to_install_handler(cls, install_playbooks):
        """
        将install playbook名列表转为对应的handler列表
        """
        install_progress_configs = filter(bool, map(cls._map_install_progress_config, install_playbooks))
        return list(map(InstallHandler, install_progress_configs))

    @classmethod
    def parse_install_tags(cls, tags):
        """
        将install tags转为install类处理对象
        """
        install_playbooks = cls._find_target_playbooks_by_tags(cls.PROCESS_INSTALL_YML, tags)
        return cls._install_playbooks_to_install_handler(install_playbooks)

    @classmethod
    def _map_install_playbook_names_in_scene(cls, scene_playbooks):
        """
        展开获取所有scene playbook中的install playbook
        """
        install_playbooks = []
        for scene_playbook in scene_playbooks:
            import_playbook_path = os.path.join(cls.SCENE_DIR, scene_playbook.get("import_playbook"))
            # 对于scene类的，进一步解析
            if "scene" in scene_playbook.get('playbook_name'):
                install_playbooks.extend(cls._parse_playbook_info(import_playbook_path))
            # 普通的playbook直接解析
            else:
                install_playbooks.append(cls._add_playbook_name(scene_playbook))
        return install_playbooks

    @classmethod
    def parse_scene_tags(cls, tags):
        """
        将scene tags转为install类处理对象
        """
        scene_playbooks = cls._find_target_playbooks_by_tags(cls.PROCESS_SCENE_YML, tags)
        install_playbooks = cls._map_install_playbook_names_in_scene(scene_playbooks)
        return cls._install_playbooks_to_install_handler(install_playbooks)

    @classmethod
    def parse_hccn(cls, tags):
        """
        将install tags转为install类处理对象
        """
        install_playbooks = cls._find_target_playbooks_by_tags(cls.PROCESS_HCCN_YML, tags)
        return cls._install_playbooks_to_install_handler(install_playbooks)

    @classmethod
    def parse_process(cls, process_type, tags):
        if process_type == InstallParser.PROCESS_TYPE_INSTALL:
            return InstallParser.parse_install_tags(tags)
        if process_type == InstallParser.PROCESS_TYPE_SCENE:
            return InstallParser.parse_scene_tags(tags)
        if process_type == InstallParser.PROCESS_TYPE_HCCN:
            return InstallParser.parse_hccn(tags)
        return []


class ProgressManager(object):
    _PROGRESS_OUTPUT_PATH = os.path.join(DEPLOY_INFO_OUTPUT_DIR, "deployer_progress_output.json")
    _OUTPUT_INTERVAL = 5
    _HOST_ERROR_STATUS = (HostStatus.FAILED, HostStatus.UNREACHABLE)

    def __init__(self, process_type, install_handlers):
        self.process_type = process_type
        self.install_handlers = install_handlers or []
        # 预载准备阶段
        self.prepare_handler = InstallHandler(PREPARE_CONFIG)
        self.prepare_handler.on_play_start(PREPARE_CONFIG.name)
        self.install_handlers = [self.prepare_handler] + self.install_handlers
        self.cur_handler_index = 0
        self.deploy_status = DeployStatus.WAIT
        self.host_status_dict = {}
        self.need_output = any((p_type in self.process_type) for p_type in InstallParser.SUPPORTED_PROCESS_TYPES)
        self._start_output_timer()

    @classmethod
    def generate_progress_manager(cls, process_type, tags):
        install_handlers = InstallParser.parse_process(process_type, tags)
        if not install_handlers:
            ERROR_MSG_LIST.append("No process type.")
        return cls(process_type, install_handlers)

    def _is_handler_existed(self):
        return self.cur_handler_index < len(self.install_handlers)

    def _output_worker(self):
        while True:
            time.sleep(self._OUTPUT_INTERVAL)
            self.output_progress_json()

    def _start_output_timer(self):
        t = threading.Thread(target=self._output_worker)
        t.setDaemon(True)
        t.start()

    @error_catcher
    def on_play_start(self, play_name, host_num):
        """
        执行某个install的可能的场景
        1. 预置的primary_plays全部被执行完
        2. 预置的primary_plays一个都没被执行
        3. 预置的primary_plays其中部分被执行（可能是限制的主机组等条件，
        遇到一个play，可能当前的场景：
        1. 该play在当前handler的primary_plays中 -> 直接触发handler的on_play_start
        # 出现任何未在当前handler中的play，代表handler已执行结束
        2. 该play未在当前handler中，属于中间多余步骤
        3. 该play未在当前handler中，属于下一个handler中的play
        """
        if not self._is_handler_existed():
            return
        if self.deploy_status == DeployStatus.WAIT:
            self.deploy_status = DeployStatus.DEPLOYING
        # 属于当前handler的play
        cur_handler = self.install_handlers[self.cur_handler_index]
        # 为0时，属于准备阶段，直接开始
        if cur_handler.is_play_in_handler(play_name):
            cur_handler.on_play_start(play_name, host_num)
        else:
            # 属于后续handler的play
            self._find_play_in_sub_handler(cur_handler, host_num, play_name)

    def _find_play_in_sub_handler(self, cur_handler, host_num, play_name):
        index = self._find_sub_handler_index(play_name)
        if index != -1:
            cur_handler.on_handler_end()
            for i in range(self.cur_handler_index + 1, index):
                self.install_handlers[i].deploy_status = DeployStatus.SKIP
                self.install_handlers[i].on_handler_end()
            self.cur_handler_index = index
            self.install_handlers[index].on_play_start(play_name, host_num)

    def _find_sub_handler_index(self, play_name):
        if self.cur_handler_index >= len(self.install_handlers) - 1:
            return -1
        for i in range(self.cur_handler_index + 1, len(self.install_handlers)):
            handler = self.install_handlers[i]
            if handler.is_play_in_handler(play_name):
                return i
        return -1

    def handle_host_status(self, host, status=HostStatus.DEPLOYING):
        if self.host_status_dict.get(host) in HOST_FINISH_STATUS:
            return
        self.host_status_dict[host] = status

    def set_all_host_status_after_deploy(self):
        for host in self.host_status_dict.keys():
            self.handle_host_status(host, HostStatus.SUCCESS)

    @error_catcher
    def on_end_all(self, stats):
        if self._is_handler_existed():
            self.install_handlers[self.cur_handler_index].on_handler_end()
        if stats.failures:
            self.deploy_status = DeployStatus.FAILED
        elif self.deploy_status != DeployStatus.FAILED:
            self.deploy_status = DeployStatus.SUCCESS
        self.set_all_host_status_after_deploy()
        self.output_progress_json()

    @error_catcher
    def on_task_start(self, task_name):
        if not self._is_handler_existed():
            return
        self.install_handlers[self.cur_handler_index].on_task_start(task_name)

    @error_catcher
    def on_task_failed(self, host, task_name, failed_info):
        self.deploy_status = DeployStatus.FAILED
        if not self._is_handler_existed():
            return
        self.handle_host_status(host, HostStatus.FAILED)
        self.install_handlers[self.cur_handler_index].on_task_failed(host, task_name, failed_info)

    @error_catcher
    def on_unreachable(self, host):
        self.deploy_status = DeployStatus.FAILED
        if not self._is_handler_existed():
            return
        self.handle_host_status(host, HostStatus.UNREACHABLE)
        self.install_handlers[self.cur_handler_index].on_unreachable(host)

    @error_catcher
    def on_task_end(self, host, task_name, deploy_status, deploy_info):
        if not self._is_handler_existed():
            return
        self.handle_host_status(host, HostStatus.DEPLOYING)
        handler = self.install_handlers[self.cur_handler_index]
        handler.on_task_end(host, task_name, deploy_status, DeployStatus.SUCCESS, deploy_info)

    @error_catcher
    def get_deployer_progress_output(self):
        if not self._is_handler_existed():
            return DeployerProgressOutput(error_msg="\n".join(ERROR_MSG_LIST))
        try:
            output = DeployerProgressOutput(
                cur_playbook=self.install_handlers[self.cur_handler_index].progress_config.name,
                playbooks=[install_handler.get_playbook_output() for install_handler in self.install_handlers],
                total_host_info=[{"ip": host, "status": status} for host, status in self.host_status_dict.items()],
                deploy_status=self.deploy_status, error_msg="\n".join(ERROR_MSG_LIST))
        except Exception:
            output = DeployerProgressOutput(deploy_status=DeployStatus.FAILED, error_msg="\n".join(ERROR_MSG_LIST))
        return output

    @error_catcher
    def output_progress_json(self):
        if not self.need_output:
            return
        if not os.path.exists(DEPLOY_INFO_OUTPUT_DIR):
            os.makedirs(DEPLOY_INFO_OUTPUT_DIR)
        with open(self._PROGRESS_OUTPUT_PATH, "w") as output_fs:
            json.dump(self.get_deployer_progress_output().to_json(), output_fs, indent=4, ensure_ascii=False)


class CallbackModule(ansible.plugins.callback.CallbackBase):
    _PROCESS_TYPE_PATTERN = re.compile(r"process_(\w+)\.yml")

    def __init__(self, display=None, options=None):
        super(CallbackModule, self).__init__(display, options)
        self.args = sys.argv
        process_type = self._parse_process_type(sys.argv)
        tags = self._find_tags(sys.argv) + ["always"]
        self.all_hosts = []
        self.progress_manager = ProgressManager.generate_progress_manager(process_type, tags)
        self._last_play_name = ""
        self._cur_play = None

    @classmethod
    def _parse_process_type(cls, args):
        for arg in args:
            search_res = re.search(cls._PROCESS_TYPE_PATTERN, arg)
            if search_res:
                return search_res.group(1)
        return ""

    @staticmethod
    def _find_tags(args):
        tags_op = "--tags"
        if tags_op in args:
            tag_index = args.index("--tags")
            if tag_index < len(args) - 1:
                return str(args[tag_index + 1]).split(",")
        return []

    def custom_on_play_start(self, play):
        super(CallbackModule, self).v2_playbook_on_play_start(play)
        if not self.all_hosts:
            self.all_hosts = [h.name for h in play.get_variable_manager()._inventory.get_hosts()]
        self.progress_manager.on_play_start(play.get_name(), len(self.all_hosts) or 1)

    def v2_playbook_on_play_start(self, play):
        # play: ansible.playbook.play.Play
        self._cur_play = play

    def v2_playbook_on_stats(self, stats):
        # stats: ansible.executor.stats.AggregateStats
        super(CallbackModule, self).v2_playbook_on_stats(stats)
        self.progress_manager.on_end_all(stats)

    def v2_playbook_on_task_start(self, task, is_conditional):
        # task: ansible.playbook.task.Task
        cur_play_name = self._cur_play.get_name().strip()
        # ansible的机制导致即使不执行的play也会启用回调事件，通过规避没有task执行的play跳过
        if cur_play_name != self._last_play_name:
            self.custom_on_play_start(self._cur_play)
            self._last_play_name = cur_play_name
        super(CallbackModule, self).v2_playbook_on_task_start(task, is_conditional)
        task_name = task.get_name()
        self.progress_manager.on_task_start(task_name)

    @staticmethod
    def _build_res_info(result):
        # result: ansible.executor.task_result.TaskResult
        host = result._host.get_name()
        task_name = result._task.get_name()
        msg = result._result.get('msg', '')
        # 获取任务的标准输出和标准错误输出
        stdout = result._result.get('stdout', '')
        stderr = result._result.get('stderr', '')
        install_std_out = result._result.get('std_out', '')
        task_result = result._result.get('result', {})
        res_info_list = []
        if msg:
            res_info_list.append("Message: {}".format(msg))
        if stdout:
            res_info_list.append("Standard Output:{}.".format(stdout))
        if stderr:
            res_info_list.append("Standard Error Output:{}.".format(stderr))
        if install_std_out:
            res_info_list.append("Task output: {}.".format(install_std_out))
        return host, task_name, task_result, res_info_list

    def v2_runner_on_ok(self, result):
        # result: ansible.executor.task_result.TaskResult
        super(CallbackModule, self).v2_runner_on_ok(result)
        host, task_name, task_result, res_info_list = self._build_res_info(result)
        deploy_status = task_result.get(DeployStatus.DEPLOY_STATUS, DeployStatus.DEPLOYING)
        self.progress_manager.on_task_end(host, task_name, deploy_status, "\n".join(res_info_list))

    def runner_on_unreachable(self, host, res):
        super(CallbackModule, self).runner_on_unreachable(host, res)
        self.progress_manager.on_unreachable(host)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        # result: ansible.executor.task_result.TaskResult
        super(CallbackModule, self).v2_runner_on_failed(result, ignore_errors)
        host, task_name, _, res_info_list = self._build_res_info(result)
        self.progress_manager.on_task_failed(host, task_name, "\n".join(res_info_list))
