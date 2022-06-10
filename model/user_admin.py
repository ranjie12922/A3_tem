# coding=utf-8
from model.user import User

from lib.helper import user_data_path


class Admin(User):
    def __init__(
        self,
        uid: int = -1,
        username: str = "",
        password: str = "",
        register_time: str = "",
        role: str = "",
    ):
        super().__init__(uid, username, password, register_time, role)

    def register_admin(self):
        user_path = user_data_path
        if not User.check_username_exist(self.username):
            with open(user_path, "a", encoding='utf-8') as a:
                tmp_str = (
                    str(self.uid)
                    + ";;;"
                    + self.username
                    + ";;;"
                    + User.encrypt_password(self.password)
                    + ";;;"
                    + self.register_time
                    + ";;;"
                    + self.role
                )
                a.write(tmp_str)
                a.write("\n")
            return True

        return False

    def __str__(self):
        return (
            f"{self.uid};;;{self.username};;;{self.password};;;"
            + f"{self.register_time};;;{self.role}"
        )
