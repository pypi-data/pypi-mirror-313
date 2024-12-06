import abc
import re
from collections import defaultdict
from string import Template
from typing import Tuple, Dict


class CmdEvent:

    @abc.abstractmethod
    def execute(self, parse_cmd_dict) -> Tuple[int, str]:
        pass


class MockCmdPattern:

    def __init__(self, cmd: str):
        self._cmd_pattern = re.compile(cmd)

    @abc.abstractmethod
    def parse(self, cmd, extend_data: Dict = None) -> Tuple[bool, Tuple[int, str]]:
        pass

    def _parse_cmd(self, cmd):
        search_res = self._cmd_pattern.search(cmd)
        if not search_res:
            return False, {}
        return True, search_res.groupdict()


class MockCmdTemplatePattern(MockCmdPattern):

    def __init__(self, cmd: str, code: int = 0, output: str = ""):
        super().__init__(cmd)
        self.code = code
        self.output_pattern = Template(output)

    def parse(self, cmd, extend_data: Dict = None):
        res, parse_dict = self._parse_cmd(cmd)
        if not res:
            return False, (-1, "")
        parse_dict.update(extend_data or {})
        return True, (self.code, self.output_pattern.safe_substitute(defaultdict(str, parse_dict)))


class MockCmdEventPattern(MockCmdPattern):

    def __init__(self, cmd: str, event):
        super().__init__(cmd)
        self.event = event

    def parse(self, cmd, extend_data: Dict = None):
        res, parse_dict = self._parse_cmd(cmd)
        if not res:
            return False, (-1, "")
        event_executor = extend_data.get(self.event)
        if not event_executor:
            raise Exception(f"Event: {self.event} not existed.")
        return True, event_executor.execute(parse_dict)
