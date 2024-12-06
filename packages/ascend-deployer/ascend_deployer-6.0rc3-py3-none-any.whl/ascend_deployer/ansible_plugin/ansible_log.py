#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import os.path
import sys
import logging
import logging.handlers
import os
import stat
import yaml

from ansible.playbook.task_include import TaskInclude
from ansible.plugins.callback.default import CallbackModule as default
from ansible.plugins.callback import Display
from ansible.utils.unsafe_proxy import AnsibleUnsafeText
from ansible import constants as C
from ansible import context

PERMS_600 = stat.S_IRUSR | stat.S_IWUSR
CURSOR_UPWARD = u'\u001b[1A'
COMPAT_OPTIONS = (('display_skipped_hosts', C.DISPLAY_SKIPPED_HOSTS),
                  ('display_ok_hosts', True),
                  ('show_custom_stats', C.SHOW_CUSTOM_STATS),
                  ('show_task_path_on_failure', False),
                  ('display_failed_stderr', False),)
replace_dict = {"{{ansible_pkg_mgr}}": "apt", "{ansible_pkg_mgr}": "apt", "{{os_and_arch}}": "CentOS_7.6_aarch64",
                "{os_and_arch}": "CentOS_7.6_aarch64"}


def replace_parameter(new_tasks):
    if new_tasks is None:
        return None
    for key, value in replace_dict.items():
        if key in new_tasks:
            return new_tasks.replace(key, value)
    return new_tasks


def get_tasks_amount(new_tasks):
    ret = 0
    dir_name = os.path.dirname(new_tasks)
    new_tasks = replace_parameter(new_tasks)
    with open(new_tasks) as f:
        docs = yaml.safe_load(f)
        for doc in docs:
            next_tasks = ""
            if isinstance(doc, dict):
                next_tasks = doc.get("import_tasks") or doc.get("include_tasks")
            if next_tasks:
                ret += get_tasks_amount(os.path.join(dir_name, next_tasks))
        ret += len(docs)
    return ret


def get_amount_in_playbook(playbook_file):
    ret = 0
    dir_name = os.path.dirname(playbook_file)
    with open(playbook_file) as f:
        docs = yaml.safe_load(f)
        for doc in docs:
            new_playbook = doc.get("import_playbook")
            if new_playbook:
                ret += get_amount_in_playbook(os.path.join(dir_name, new_playbook))
            new_tasks = doc.get("import_tasks")
            if new_tasks:
                ret += get_tasks_amount(os.path.join(dir_name, new_tasks))
            cur_tasks = doc.get("tasks")
            if cur_tasks:
                ret += len(cur_tasks)
                for task in cur_tasks:
                    next_tasks = task.get("import_tasks") or task.get("include_tasks")
                    if next_tasks:
                        ret += get_tasks_amount(os.path.join(dir_name, next_tasks))
    return ret


class AnsibleFormatException(Exception):
    pass


class CallbackModule(default):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'ansible_log'

    def __init__(self):

        self._play = None
        self._last_task_banner = None
        self._last_task_name = None
        self._task_type_cache = {}
        self._playbook_name = None
        self._task_process = 0
        self._task_amount = 0
        self._lines_num = 0
        self._extra_msg = []
        self._fatal_flag = False
        self._is_dl_install = False
        display = LogDisplay()
        super(CallbackModule, self).__init__()
        self._display = display

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'install_info.yaml'), 'r') as f:
            self._install_info = yaml.safe_load(f)

    @staticmethod
    def _parse_msg(_msg):
        if isinstance(_msg, list):
            CallbackModule._check_msg_list(_msg)
            msg = ';'.join(_msg)
        elif isinstance(_msg, str):
            msg = _msg
        elif isinstance(_msg, AnsibleUnsafeText):
            msg = str(_msg)
        else:
            msg = ''
        msg = msg.split("=>")[0]
        return msg if msg.startswith('[ASCEND]') else ''

    @staticmethod
    def _check_msg_list(msg_list):
        for str_item in msg_list:
            if not isinstance(str_item, str):
                raise AnsibleFormatException()

    def set_options(self, task_keys=None, var_options=None, direct=None):

        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        for option, constant in COMPAT_OPTIONS:
            try:
                value = self.get_option(option)
            except (AttributeError, KeyError):
                value = constant
            self.set_option(option, value)

    def v2_runner_on_skipped(self, result):
        super(CallbackModule, self).v2_runner_on_skipped(result)
        if isinstance(result._task, TaskInclude):
            self._task_process += get_tasks_amount(
                os.path.join(os.path.dirname(result._task.get_path()), result._task.args.get('_raw_params')))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        super(CallbackModule, self).v2_runner_on_unreachable(result)
        show_reason = 'please check log at {HOME}/.log/'
        for record in result._result.get('results', []):
            if not record.get('failed'):
                continue
            reason_msg = self._try_parse_msg(record.get('msg'))
            if reason_msg:
                show_reason = reason_msg
                break
        else:
            reason_msg = ''
            if hasattr(result, '_result'):
                reason_msg = self._try_parse_msg(getattr(result, '_result').get('msg', ''))
            if reason_msg:
                show_reason = reason_msg

        if not ignore_errors:
            self._fatal_flag = True
            self._extra_msg.append("{:<50}".format("[%s]: FAILED! %s" % (
                result._host.get_name(), show_reason)))
            self.screen_display()

    def v2_runner_on_unreachable(self, result):
        super(CallbackModule, self).v2_runner_on_unreachable(result)
        host_label = result._host.get_name()
        msg = "fatal: [%s]: UNREACHABLE! => %s" % (host_label, result._result.get('msg'))
        self._extra_msg.append(msg)
        if not result._task.ignore_unreachable:
            self._fatal_flag = True
            self.screen_display()

    def v2_runner_on_start(self, host, task):
        self._display.display(" [started %s on %s]" % (task, host), color=C.COLOR_OK)

    def v2_runner_on_ok(self, result):
        super(CallbackModule, self).v2_runner_on_ok(result)
        msg = result._result.get('msg')
        msg = self._try_parse_msg(msg)
        if msg:
            host_label = result._host.get_name()
            extra = "{:<50}".format("%s => %s " % (msg.replace("[ASCEND]", ""), host_label))
            self._extra_msg.append(extra)

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)

            self._display.display(
                u"%s : ok=%d changed=%d unreachable=%d failed=%d skipped=%d rescued=%d ignored=%d" % (
                    h,
                    t['ok'],
                    t['changed'],
                    t['unreachable'],
                    t['failures'],
                    t['skipped'],
                    t['rescued'],
                    t['ignored'],
                )
            )
        if self._is_dl_install:
            if self._fatal_flag:
                self._display.display("[ERROR]Ascend DL deployed failed --ascend-deployer", color=C.COLOR_ERROR)
            else:
                self._display.display("[INFO]Ascend DL deployed success --ascend-deployer")
        if not self._fatal_flag:
            self._extra_msg.append("ascend deployer processed success")

        self._task_process = self._task_amount
        self.screen_display()

    def v2_playbook_on_start(self, playbook):
        tags = context.CLIARGS.get('tags')
        if 'dl' in tags:
            self._is_dl_install = True
        self._playbook_name = os.path.basename(playbook._file_name).split(".")[0]
        self._task_amount = get_amount_in_playbook(playbook._file_name)

    def ordinary_msg_scene(self, file_name=""):
        msg = str(self._playbook_name)
        if msg.startswith("process"):
            file_name = file_name.replace("task", "install")
            msg_words = file_name.split("_")
            if len(msg_words) >= 2:
                tmp_msg = None
                for doc in self._install_info:
                    part = doc.get(msg_words[0], {})
                    if part:
                        tmp_msg = part.get(msg_words[1], "")
                    if tmp_msg:
                        return tmp_msg
            msg = " ".join(msg_words)
            return msg
        else:
            msg = msg.replace("_", " ")
            return msg

    def search_common_msg(self, file_name):
        for doc in self._install_info:
            res = doc.get("common", {}).get(file_name, "")
            if res:
                return res
        return None

    def get_terminal_size(self):
        try:
            return os.get_terminal_size()
        except (AttributeError, OSError):
            import subprocess
            try:
                size = subprocess.check_output(['stty', 'size']).split()
                return int(size[1]), int(size[0])
            except (subprocess.CalledProcessError, IndexError, ValueError):
                return 84, 270

    def screen_display(self, file_name=""):
        if self._playbook_name is None:
            return

        msg = self.search_common_msg(self._playbook_name) or self.search_common_msg(file_name)
        if not msg:
            msg = self.ordinary_msg_scene(file_name)
        title_bar = "{:<50}".format(msg)
        action = "=" * (int(min(1, self._task_process / self._task_amount) * 50))
        if self._task_process == self._task_amount:
            action += "="
        else:
            action += ">"
        task_bar = "task info:{:<80}".format(self._last_task_name)
        process_bar = "[{:-<51}]".format(action)
        bar_list = [title_bar, task_bar, process_bar]
        bar_list.extend(self._extra_msg)
        if self._task_process != 0:
            for i in range(0, self._lines_num):
                sys.stdout.write(CURSOR_UPWARD)
        screen_prints = "\r" + "\n".join(bar_list) + "\n"
        sys.stdout.write(screen_prints)
        screen_size = self.get_terminal_size()[0]
        backward = 0
        for bars in bar_list:
            for bar in bars.split("\n"):
                backward += len(bar) // screen_size
        self._lines_num = screen_prints.count("\n") + backward

    def confirm_playbook_name(self, path):
        if "mindx" in path:
            start_index = path.find('/mindx.') + len('/mindx.')
            end_index = path.find('/', start_index)
            self._playbook_name = path[start_index:end_index]

    def _print_task_banner(self, task):
        args = ''
        if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
            args = u', '.join(u'%s=%s' % a for a in task.args.items())
            args = u' %s' % args

        prefix = self._task_type_cache.get(task._uuid, 'TASK')

        task_name = self._last_task_name
        if task_name is None:
            task_name = task.get_name().strip()
        path = task.get_path()
        if path:
            log_write.info(u"task path: %s" % path)
            self.confirm_playbook_name(path)
            file_name = os.path.basename(path.split(":")[0]).split(".")[0]
        log_write.info(u"%s [%s%s]" % (prefix, task_name, args))
        self.screen_display(file_name=file_name)
        self._task_process += 1

        self._last_task_banner = task._uuid

    def _task_start(self, task, prefix=None):
        super(CallbackModule, self)._task_start(task, prefix)

    def _handle_warnings(self, res):
        if C.ACTION_WARNINGS:
            if 'deprecations' in res and res['deprecations']:
                for warning in res['deprecations']:
                    self._display.display(**warning)
                del res['deprecations']
            else:
                super(CallbackModule, self)._handle_warnings(res)

    def _try_parse_msg(self, item):
        try:
            return self._parse_msg(item)
        except AnsibleFormatException:
            debug_msg = "{:<50}".format("bad grammar at %s" % self._last_task_name)
            self._extra_msg.append(debug_msg)
            return ''


class LogDisplay(Display):
    def __init__(self):
        super(LogDisplay, self).__init__()

    def display(self, msg, color=None, stderr=False, screen_only=False, log_only=False, newline=True):
        fatal_line = msg.startswith(u'fatal')
        if fatal_line or color == C.COLOR_ERROR:
            log_write.error(msg)
        else:
            log_write.info(msg)


class RotatingFileHandler(logging.handlers.RotatingFileHandler):

    def doRollover(self):
        largest_backfile = "{}.{}".format(self.baseFilename, 5)
        if os.path.exists(largest_backfile):
            os.chmod(largest_backfile, PERMS_600)
        os.chmod(self.baseFilename, stat.S_IRUSR)
        logging.handlers.RotatingFileHandler.doRollover(self)
        os.chmod(self.baseFilename, PERMS_600)


class BasicLogConfig(object):
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    LOG_FILE = "{}/.log/mindx-dl-install.log".format(os.environ.get("HOME", "/root"))
    LOG_PATH = "{}/.log".format(os.environ.get("HOME", "/root"))
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_FORMAT_STRING_ANSIBLE = \
        "%(message)s "
    LOG_FORMAT_STRING_DEPLOYER = \
        "%(message)s "
    LOG_LEVEL = logging.INFO

    ROTATING_CONF = dict(
        mode='a',
        maxBytes=20 * 1024 * 1024,
        backupCount=5,
        encoding="UTF-8")
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    if not os.path.exists(LOG_FILE):
        os.close(os.open(LOG_FILE, os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR))
    else:
        os.chmod(LOG_FILE, stat.S_IRUSR | stat.S_IWUSR)


def get_logger_ansible(name):
    """
    get_logger
    """
    log_conf = BasicLogConfig()
    logger = logging.getLogger(name)
    rotating_handler = RotatingFileHandler(
        filename=log_conf.LOG_FILE, **log_conf.ROTATING_CONF)
    log_formatter = logging.Formatter(
        log_conf.LOG_FORMAT_STRING_ANSIBLE, log_conf.LOG_DATE_FORMAT)
    rotating_handler.setFormatter(log_formatter)
    logger.addHandler(rotating_handler)
    logger.setLevel(log_conf.LOG_LEVEL)
    return logger


def get_logger_deploy(name):
    """
    get_logger
    """
    log_conf = BasicLogConfig()
    logger = logging.getLogger(name)
    rotating_handler = RotatingFileHandler(
        filename=log_conf.LOG_FILE, **log_conf.ROTATING_CONF)
    log_formatter = logging.Formatter(
        log_conf.LOG_FORMAT_STRING_DEPLOYER, log_conf.LOG_DATE_FORMAT)
    rotating_handler.setFormatter(log_formatter)
    ch = logging.StreamHandler()
    ch.setLevel('INFO')
    ch.setFormatter(log_formatter)
    logger.addHandler(rotating_handler)
    logger.addHandler(ch)
    logger.setLevel(log_conf.LOG_LEVEL)
    return logger


log_write = get_logger_ansible("ansible")
log_stdout = get_logger_deploy("deployer")
