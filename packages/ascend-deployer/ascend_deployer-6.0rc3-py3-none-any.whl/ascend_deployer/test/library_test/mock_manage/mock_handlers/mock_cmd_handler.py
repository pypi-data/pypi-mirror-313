from typing import List, Dict

from library_test.mock_manage.mock_model.cmd_pattern import MockCmdPattern


class MockSpCmdResultStdout:

    def __init__(self, output=""):
        self.output = output

    def readlines(self):
        return self.output.splitlines()


class MockSpCmdResult:

    def __init__(self, code, output, err=""):
        self.returncode = code
        self.output = output
        self.err = err
        self.stdout = MockSpCmdResultStdout(output)

    def communicate(self, *args, **kwargs):
        return self.output, self.err


class MockCmdHandler:

    def __init__(self, cmd_patterns, extend_data: Dict):
        self.extend_data = extend_data
        self._cmd_patterns: List[MockCmdPattern] = cmd_patterns

    # 处理subprocess的结果
    def Popen(self, cmd_args: List[str], *args, **kwargs):
        cmd = " ".join(cmd_args)
        code, output = self.find_cmd_pattern(cmd)
        return MockSpCmdResult(code, output)

    def find_cmd_pattern(self, cmd):
        for pattern in self._cmd_patterns:
            parse_res, parse_output = pattern.parse(cmd, self.extend_data)
            if parse_res:
                return parse_output
        return -1, f"Testcase error, no cmd pattern found. cmd: {cmd}"

    def run_command(self, cmd):
        code, output = self.find_cmd_pattern(cmd)
        return code, output, ""
