import json
from typing import Dict

from library_test.mock_manage.mock_handlers.mock_cmd_handler import MockCmdHandler


class AnsibleModule:

    def __init__(self, params: Dict, cmd_handler: MockCmdHandler, *args, **kwargs):
        self.params = params
        self.cmd_handler = cmd_handler

    class FailJson(Exception):
        pass

    class ExitJson(Exception):
        pass

    def fail_json(self, **kwargs):
        res = json.dumps(kwargs, indent=4)
        print(res)
        raise AnsibleModule.FailJson(res)

    def exit_json(self, **kwargs):
        res = json.dumps(kwargs, indent=4)
        print(res)
        raise AnsibleModule.ExitJson(res)

    def run_command(self, cmd, *args, **kwargs):
        return self.cmd_handler.run_command(cmd)
