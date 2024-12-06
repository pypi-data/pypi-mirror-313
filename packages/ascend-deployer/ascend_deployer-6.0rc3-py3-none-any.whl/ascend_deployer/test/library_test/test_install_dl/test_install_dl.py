from abc import ABC

from library_test.base_test import BaseTest


class TestInstallDl(BaseTest, ABC):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.mock_manager.start_subprocess_patcher(cls.get_module_path(), "sp")
        cls.mock_manager.start_tar_open_patcher(cls.get_module_path())

    @classmethod
    def get_module_path(cls):
        return "ascend_deployer.module_utils.dl"
