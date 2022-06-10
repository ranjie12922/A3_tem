# coding=utf-8

import random
import re
from warnings import resetwarnings

from lib.helper import user_data_path, get_day_from_timestamp


class User:
    current_login_user = None

    def __init__(
        self,
        uid: int = -1,
        username: str = "",
        password: str = "",
        register_time: str = "",
        role: str = "",
    ):
        self.role = role
        self.register_time = register_time
        self.username = username
        self.password = password
        self.uid = uid

    def __str__(self):
        return (
            f"{self.uid};;;{self.username};;;{self.password};;;"
            "f{self.register_time};;;{self.role}"
        )

    @classmethod
    def validate_username(cls, username):
        num_name = re.compile("^[A-Za-z_]*$")
        if num_name.search(username):
            return True
        else:
            return False

    @classmethod
    def validate_password(cls, password):
        if len(password) >= 8:
            return True
        else:
            return False

    @classmethod
    def validate_email(cls, email):
        if len(email) <= 8:
            return False

        if "@" not in email:
            return False

        if not email.endswith(".com"):
            return False
        return True

    @classmethod
    def clear_user_data(cls):
        user_path = user_data_path
        with open(user_path, "w") as w_clear:
            w_clear.write("")

    @classmethod
    def authenticate_user(cls, username, password):
        """
        “uid;;;username;;;password;;;register_time;;;role”
        """
        user_path = user_data_path
        with open(user_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                tmp_line = line.strip("\n").split(";;;")
                if len(tmp_line) > 2:
                    if username == tmp_line[1] and cls.encrypt_password(
                        password
                    ) == tmp_line[2].strip("\n"):
                        return line
                line = r.readline()
        return None

    @classmethod
    def check_username_exist(cls, username):
        """
        “uid;;;username;;;password;;;register_time;;;role”
        """
        user_path = user_data_path
        with open(user_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                tmp_line = line.strip("\n").split(";;;")
                if len(tmp_line) >= 5:
                    if username == tmp_line[1]:
                        return True
                # print(line)
                line = r.readline()
        return False

    @classmethod
    def generate_unique_user_id(cls):
        user_path = user_data_path

        all_ids = []
        with open(user_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                tmp_li = line.split(";;;")
                if len(tmp_li) > 2:
                    all_ids.append(int(tmp_li[0].strip("}")))
                line = r.readline()

        unique = False
        id = 0
        while not unique:
            id = random.randrange(100000, 1000000)
            if id not in all_ids:
                unique = True

        return id

    @classmethod
    def encrypt_password(cls, password):
        input_str = str(password)
        all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        input_len = len(input_str)
        punctuation_len = len(all_punctuation)
        dic = {
            1: all_punctuation[input_len % punctuation_len],
            2: all_punctuation[input_len % 5],
            3: all_punctuation[input_len % 10],
        }
        result = "^^^"
        for i in range(1, len(input_str) + 1):
            if i % 3 == 0:
                count = 3
            else:
                count = i % 3
            result += count * dic[count]
            result += input_str[i - 1]
            result += count * dic[count]
        result += "$$$"
        return result

    @classmethod
    def register_user(cls, username, password, register_time, role, email):
        user_path = user_data_path

        if not cls.check_username_exist(username):
            with open(user_path, "a", encoding='utf-8') as a:
                tmp_str = (
                    str(cls.generate_unique_user_id())
                    + ";;;"
                    + username
                    + ";;;"
                    + cls.encrypt_password(password)
                    + ";;;"
                    + cls.date_conversion(register_time)
                    + ";;;"
                    + role
                    + ";;;"
                    + email
                )
                if role == "instructor":
                    tmp_str = tmp_str + ";;;;;;;;;"
                a.write(tmp_str)
                a.write("\n")

    @classmethod
    def date_conversion(cls, register_time):
        register_time = int(register_time) / 1000
        year_s = 31556926
        month_s = 2629743
        day_s = 86400
        hour_s = 3600

        year = 1970 + (register_time // year_s)
        remaining = register_time % year_s

        month = remaining // month_s + 1
        remaining = remaining % month_s

        day = get_day_from_timestamp(register_time)
        remaining = register_time % day_s

        hour = remaining // hour_s
        remaining = remaining % hour_s

        minute = remaining // 60
        remaining = remaining % 60

        second = remaining / 1

        if (hour + 11) > 23:
            hour = (hour + 11) - 24
            day = day + 1
        else:
            hour = hour + 11

        return (
            f"{int(year)}-"
            + f"{int(month)}-"
            + f"{int(day)}_"
            + f"{int(hour)}:"
            + f"{int(minute)}:"
            + "{:.3f}".format(second)
        )
