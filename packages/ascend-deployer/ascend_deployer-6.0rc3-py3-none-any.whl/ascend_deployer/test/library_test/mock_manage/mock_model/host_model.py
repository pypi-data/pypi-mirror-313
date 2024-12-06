from typing import List, Dict, Tuple


class UserModel:

    def __init__(self, user, uid, is_cur_user=False):
        self.user = user
        self.uid = str(uid)
        self.is_cur_user = is_cur_user


class MockGrpStructGroup:

    def __init__(self, gr_name, gr_gid):
        self.gr_name = gr_name
        self.gr_gid = gr_gid


class GroupModel:

    def __init__(self, group, gid, users: List[Dict]):
        self.group = group
        self.gid = str(gid)
        self.users = [UserModel(**user) for user in users]

    def get_grp_struct_group(self):
        return MockGrpStructGroup(self.group, self.gid)


class HostModel:

    def __init__(self, ip: str, cpu_arch, groups: List[Dict], envs: Dict):
        self.ip = ip
        self.cpu_arch = cpu_arch
        self.groups = [GroupModel(**group) for group in groups]
        self.envs = envs

    def get_cur_group_and_user(self) -> Tuple[GroupModel, UserModel]:
        for group in self.groups:
            for user in group.users:
                if user.is_cur_user:
                    return group, user
        raise Exception("No cur user!")

    def query_group(self, group_name):
        for group in self.groups:
            if group.group == group_name:
                return group
        raise Exception(f"Not found group: {group}!")

    def switch_user(self, user_name="", uid=None):
        group, user = self.get_cur_group_and_user()
        user.is_cur_user = False
        for group in self.groups:
            for user in group.users:
                if user.user == user_name or user.uid == uid:
                    user.is_cur_user = True

    def get_grp_struct_group(self, group_name):
        return self.query_group(group_name).get_grp_struct_group()

    def get_uid(self):
        group, user = self.get_cur_group_and_user()
        return user.uid

    def get_gid(self):
        group, user = self.get_cur_group_and_user()
        return group.gid

    def add_user(self, user_name, uid="", gid=""):
        group = self.groups[0]
        if gid:
            group = [group for group in self.groups if group.gid == gid][0]
        group.users.append(UserModel(user_name, uid or str(int(group.users[-1].uid) + 1)))
