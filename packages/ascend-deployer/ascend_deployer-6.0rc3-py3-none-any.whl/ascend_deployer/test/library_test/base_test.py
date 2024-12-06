import abc
import importlib
import json
import sys
import unittest
from typing import Dict

from library_test.mock_manage.mock_manager import MockManager
from library_test.mock_manage.mock_model.testcase_model import TestCase


class BaseTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    @classmethod
    def replace_module(cls, source_path, target_path):
        replacement_module = importlib.import_module(target_path)
        sys.modules[source_path] = replacement_module

    @classmethod
    def replace_ansible_module(cls):
        cls.replace_module("ansible.module_utils", "ascend_deployer.module_utils")
        cls.replace_module("ansible.module_utils.basic", "library_test.mock_manage.mock_model.mock_ansible_module")

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.replace_ansible_module()


class BaseLibraryTest(BaseTest):

    def setUp(self) -> None:
        super().setUp()

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        test_case = TestCase(cls.get_testcase_path())
        cls.mock_manager = MockManager(test_case)
        cls.mock_manager.mock_file_handler.start_mock()  # 位置很关键，file_handler必须先执行
        cls.mock_manager.mock_file_handler.add_file(test_case.file_config)
        cls.mock_manager.start_subprocess_patcher("ascend_deployer.module_utils.common_info")
        cls.mock_manager.start_ansible_module_patcher(cls.get_module_path())
        cls.mock_manager.start_uid_patcher(cls.get_module_path())
        cls.mock_manager.start_gid_patcher(cls.get_module_path())
        cls.mock_manager.start_arch_patcher(cls.get_module_path())
        cls.mock_manager.start_tar_open_patcher(cls.get_module_path())
        cls.mock_manager.start_env_patcher(cls.get_module_path())

    @classmethod
    def parse_context_exception(cls, context) -> Dict:
        return json.loads(str(context.exception))

    @classmethod
    @abc.abstractmethod
    def get_testcase_path(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def get_module_path(cls):
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        cls.mock_manager.mock_file_handler.end_mock()
