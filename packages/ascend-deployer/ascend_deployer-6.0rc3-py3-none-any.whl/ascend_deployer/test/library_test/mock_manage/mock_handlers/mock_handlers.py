from typing import Dict


class MockEnvHandler:

    def __init__(self, default_env: Dict = None):
        self.env_dict = {}
        self.env_dict.update(default_env or {})

    def add_env(self, key, value):
        self.env_dict[key] = value

    def get(self, key):
        return self.env_dict.get(key, "")

    def __getitem__(self, key):
        return self.env_dict.get(key, "")

    def __setitem__(self, key, value):
        self.env_dict[key] = value

