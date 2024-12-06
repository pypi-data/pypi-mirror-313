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
from ansible.plugins.callback import default

OPTIONS = (('show_task_path_on_failure', True),)


class CallbackModule(default.CallbackModule):
    """
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'standard'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self._display.columns = min(self._display.columns, 120)
        self.last_play_name = None

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)
        options = list(OPTIONS)
        if hasattr(default, "COMPAT_OPTIONS"):
            options.extend(default.COMPAT_OPTIONS or [])
        for k, v in options:
            self.set_option(k, v)

    def v2_playbook_on_task_start(self, task, is_conditional):
        name = self._play.get_name().strip()
        if name != self.last_play_name:
            super(CallbackModule, self).v2_playbook_on_play_start(self._play)
            self.last_play_name = name
        self._task_start(task, prefix='TASK')

    def v2_playbook_on_play_start(self, play):
        self._play = play
