import os.path
from typing import List, Dict

import yaml

from library_test.mock_manage.mock_model.cmd_pattern import MockCmdTemplatePattern, MockCmdEventPattern, MockCmdPattern
from library_test.mock_manage.mock_model.host_model import HostModel


def trans_to_abs_path(src_path, real_path):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(src_path)), real_path))


def read_yml(yaml_file_path):
    with open(yaml_file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)


def yml_to_entity(config_path, entity_class):
    return entity_class(**read_yml(config_path))


def to_entity_list(dict_list: List[Dict], entity_class):
    return [entity_class(**item) for item in (dict_list or [])]


def read_file(file_path):
    with open(file_path) as f:
        return f.read()


class RelYmlConfigFile:

    def __init__(self, abs_config_path: str):
        self.abs_config_path = abs_config_path

    def _trans_to_abs_paths(self, config_paths):
        return [trans_to_abs_path(self.abs_config_path, config_path) for config_path in config_paths]

    def _trans_to_abs_path(self, config_path):
        return self._trans_to_abs_paths([config_path])[0]

    def _to_entity(self, entity_class):
        return yml_to_entity(self.abs_config_path, entity_class)

    def _merge_configs_dict(self, config_paths):
        res = {}
        for config_abs_path in self._trans_to_abs_paths(config_paths):
            res.update(read_yml(config_abs_path))
        return res


class FileModel:

    def __init__(self, path, template=""):
        self.path = path
        self.template = template


class FileConfigEntity:

    def __init__(self, files: List[Dict] = None, dirs: List[str] = None):
        self.files = [FileModel(**file) for file in (files or [])]
        self.dirs = dirs or []


class FileYmlConfig(RelYmlConfigFile):

    def __init__(self, abs_config_path: str):
        super().__init__(abs_config_path)
        file_entity: FileConfigEntity = self._to_entity(FileConfigEntity)
        self.files = file_entity.files
        for file in self.files:
            if file.template:
                file.template = read_file(self._trans_to_abs_path(file.template))
        self.dirs = file_entity.dirs


class FileConfigGroup:

    def __init__(self, file_config_paths: List[str]):
        file_configs = list(map(FileYmlConfig, file_config_paths))
        self.dirs = []
        self.files = []
        for file_config in file_configs:
            self.dirs.extend(file_config.dirs)
            self.files.extend(file_config.files)


class CmdConfigEntity:

    def __init__(self, output_cmds: List[Dict] = None, event_cmds: List[Dict] = None):
        self.output_cmds = to_entity_list(output_cmds, MockCmdTemplatePattern)
        self.event_cmds = to_entity_list(event_cmds, MockCmdEventPattern)


class CmdYmlConfig(RelYmlConfigFile):

    def __init__(self, abs_config_path):
        super().__init__(abs_config_path)
        cmd_config_entity: CmdConfigEntity = self._to_entity(CmdConfigEntity)
        self.cmd_patterns: List[MockCmdPattern] = []
        self.cmd_patterns.extend(cmd_config_entity.output_cmds)
        self.cmd_patterns.extend(cmd_config_entity.event_cmds)


class CmdConfigGroup:

    def __init__(self, cmd_config: List[str]):
        cmd_configs = list(map(CmdYmlConfig, cmd_config))
        self.cmd_patterns: List[MockCmdPattern] = []
        for cmd_config in cmd_configs:
            self.cmd_patterns.extend(cmd_config.cmd_patterns)
        # 以写后面的配置为高优先级
        self.cmd_patterns = list(reversed(self.cmd_patterns))


class TestCaseEntity:

    def __init__(self, ansible_module: List[str], host_config: str, file_config: List[str], cmd_config: List[str]):
        self.ansible_module = ansible_module
        self.host_config = host_config
        self.file_config = file_config
        self.cmd_config = cmd_config


class TestCase(RelYmlConfigFile):

    def __init__(self, abs_config_path):
        super().__init__(abs_config_path)
        test_case_entity: TestCaseEntity = self._to_entity(TestCaseEntity)
        self.ansible_module_data = self._merge_configs_dict(test_case_entity.ansible_module)
        self.host_model: HostModel = yml_to_entity(self._trans_to_abs_path(test_case_entity.host_config), HostModel)
        self._file_config_group = FileConfigGroup(self._trans_to_abs_paths(test_case_entity.file_config))
        self._cmd_config_group = CmdConfigGroup(self._trans_to_abs_paths(test_case_entity.cmd_config))

    @property
    def file_config(self) -> FileConfigGroup:
        return self._file_config_group

    @property
    def cmd_patterns(self):
        return self._cmd_config_group.cmd_patterns
