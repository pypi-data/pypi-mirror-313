import os

from library_test.test_install_dl.test_install_dl import TestInstallDl

TESTCASE_DIR = os.path.join(os.path.dirname(__file__), "testcase")


class TestNpuExporter(TestInstallDl):
    NpuExporterModule = "ascend_deployer.library.install_npu_exporter"

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # cls.mock_manager.start_ansible_module_patcher(cls.NpuExporterModule)

    @classmethod
    def get_module_path(cls):
        return "ascend_deployer.library.install_npu_exporter"

    @classmethod
    def get_testcase_path(cls):
        return os.path.join(TESTCASE_DIR, "arch64_install_npu_exporter_success.yml")

    def test(self):
        from ascend_deployer.library.install_npu_exporter import NpuExporterInstaller
        NpuExporterInstaller().run()
