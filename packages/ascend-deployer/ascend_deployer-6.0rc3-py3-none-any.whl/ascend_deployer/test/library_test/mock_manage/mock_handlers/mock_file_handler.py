import os.path

from pyfakefs.fake_filesystem_unittest import Patcher

from library_test.mock_manage.mock_model.testcase_model import FileConfigGroup


class MockTarInfo:

    def __init__(self, name, size=0, mode=0o644, mtime=0, uid=0, gid=0, uname="root", gname="root"):
        self.name = name
        self.size = size
        self.mode = mode
        self.mtime = mtime
        self.uid = uid
        self.gid = gid
        self.uname = uname
        self.gname = gname


class MockFileHandler:

    def __init__(self):
        self.patcher = Patcher()

    def start_mock(self):
        self.patcher.setUp()

    def add_file(self, file_config: FileConfigGroup):
        for mock_dir in file_config.dirs:
            self.patcher.fs.create_dir(mock_dir)
        for mock_file in file_config.files:
            self.patcher.fs.create_file(mock_file.path, contents=mock_file.template)

    def end_mock(self):
        self.patcher.tearDown()


class MockTarContext:

    def __init__(self, mock_file_handler: MockFileHandler, file_path, members: FileConfigGroup):
        self.mock_file_handler = mock_file_handler
        self.file_path = file_path
        self.file_name = os.path.basename(file_path).replace(".tar", "").replace(".gz", "")
        self.members = members

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def extractall(self, extra_dir):
        self.mock_file_handler.patcher.fs.create_dir(os.path.join(extra_dir, self.file_name))

    def getmembers(self):
        return self.members


class MockCompressFileHandler:

    def __init__(self, mock_file_handler: MockFileHandler, members: FileConfigGroup):
        self.mock_file_handler = mock_file_handler
        self.members = members

    def tar_open(self, file_path, mode="r", *args, **kwargs):
        return MockTarContext(self.mock_file_handler, file_path, self.members)
