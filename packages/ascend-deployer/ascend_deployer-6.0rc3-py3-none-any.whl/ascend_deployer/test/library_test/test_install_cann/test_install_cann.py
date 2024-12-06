import os.path
from abc import ABC

from library_test.base_test import BaseTest
from library_test.mock_manage.mock_model.mock_ansible_module import AnsibleModule

TESTCASE_DIR = os.path.join(os.path.dirname(__file__), "testcase")


class TestInstallCann(BaseTest, ABC):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.mock_manager.start_subprocess_patcher(cls.get_module_path(), "sp")

    @classmethod
    def get_module_path(cls):
        return "ascend_deployer.library.install_cann"

    def run_test(self):
        from ascend_deployer.library import install_cann
        install_cann.main()


class TestInstallCannCase1(TestInstallCann):

    @classmethod
    def get_testcase_path(cls):
        return os.path.join(TESTCASE_DIR, "arch64_install_toolkit_success.yml")

    def test(self):
        with self.assertRaises(AnsibleModule.ExitJson) as context:
            self.run_test()
        res = self.parse_context_exception(context)
        self.assertIn("success", res.get("stdout"))


class TestInstallCannCase2(TestInstallCann):

    @classmethod
    def get_testcase_path(cls):
        return os.path.join(TESTCASE_DIR, "arch64_install_kernels_success.yml")

    def test(self):
        with self.assertRaises(AnsibleModule.ExitJson) as context:
            self.run_test()
        res = self.parse_context_exception(context)
        self.assertIn("success", res.get("stdout"))
