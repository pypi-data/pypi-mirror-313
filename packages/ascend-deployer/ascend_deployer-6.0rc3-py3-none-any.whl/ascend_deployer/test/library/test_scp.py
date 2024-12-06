from unittest.mock import patch, MagicMock

from library_test.base_test import BaseTest


class AnsibleModuleMocker:
    def __init__(self, *args, **kwargs):
        pass


class TestScp(BaseTest):

    def test_run_cmd(self, ):
        from ascend_deployer.library.scp import Scp
        patcher = patch("ascend_deployer.library.scp.sp")
        sp_mocker = patcher.start()
        ansible_module_pather = patch("ascend_deployer.library.scp.AnsibleModule")
        ansible_module_pather.start()
        res_mocker = MagicMock()
        res_mocker.communicate.return_value = "", ""
        res_mocker.returncode = 1
        sp_mocker.Popen.return_value = res_mocker
        Scp()._run_cmd("abc")
