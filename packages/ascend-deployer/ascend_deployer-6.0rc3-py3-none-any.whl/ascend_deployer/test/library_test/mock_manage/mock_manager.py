import functools
from unittest.mock import patch, MagicMock

from library_test.mock_manage.mock_handlers.mock_cmd_handler import MockCmdHandler
from library_test.mock_manage.mock_handlers.mock_file_handler import MockFileHandler, MockCompressFileHandler
from library_test.mock_manage.mock_handlers.mock_handlers import MockEnvHandler
from library_test.mock_manage.mock_model.mock_ansible_module import AnsibleModule
from library_test.mock_manage.mock_model.testcase_model import TestCase


# 被该装饰器修饰的函数，外部入参为module路径，函数内接到的参数为mocker
def patch_handle(attr=""):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, module_path, inner_attr=""):
            try:
                path = module_path + "." + (inner_attr or attr)
                patcher = patch(path)
                mocker = patcher.start()
                func(self, mocker)
            except (ImportError, AttributeError) as e:
                print(f"[WARNING]{str(e)}")
                return

        return wrapper

    return decorator


class MockManager:

    def __init__(self, test_case: TestCase):
        self.test_case = test_case
        extend_data = self.init_extend_data(self.test_case)
        self.host_model = self.test_case.host_model
        self.mock_file_handler = MockFileHandler()
        self.mock_env_handler = MockEnvHandler(self.test_case.host_model.envs)
        self.mock_zip_handler = MockCompressFileHandler(self.mock_file_handler)
        self.mock_cmd_handler = MockCmdHandler(self.test_case.cmd_patterns, extend_data)

    @staticmethod
    def init_extend_data(test_case: TestCase):
        host_data = test_case.host_model
        res = {
            "ip": host_data.ip,
        }
        res.update({("env." + k): v for k, v in test_case.host_model.envs.items()})
        return res

    @patch_handle(attr="subprocess")
    def start_subprocess_patcher(self, mocker):
        mocker.PIPE = 0
        mocker.Popen = MagicMock()
        mocker.Popen.side_effect = self.mock_cmd_handler.Popen

    @patch_handle(attr="AnsibleModule")
    def start_ansible_module_patcher(self, mocker):
        mocker.side_effect = functools.partial(AnsibleModule, self.test_case.ansible_module_data, self.mock_cmd_handler)

    @patch_handle(attr="os.getuid")
    def start_uid_patcher(self, mocker):
        mocker.side_effect = self.host_model.get_uid

    @patch_handle(attr="os.getgid")
    def start_gid_patcher(self, mocker):
        mocker.side_effect = self.host_model.get_gid

    @patch_handle(attr="platform.machine")
    def start_arch_patcher(self, mocker):
        mocker.return_value = self.host_model.cpu_arch

    @patch_handle(attr="tarfile.open")
    def start_tar_open_patcher(self, mocker):
        mocker.side_effect = self.mock_zip_handler.tar_open

    @patch_handle(attr="grp")
    def start_grp_patcher(self, mocker):
        mocker.getgrnam = MagicMock()
        mocker.getgrnam.side_effect = self.host_model.get_cur_group_and_user

    def start_env_patcher(self, module_path):
        try:
            path = module_path + ".os.environ"
            patcher = patch.dict(path, self.mock_env_handler.env_dict, clear=True)
            patcher.start()
        except (ImportError, AttributeError) as e:
            print(f"[WARNING]{str(e)}")
            return
