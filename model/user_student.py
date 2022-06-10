from model.user import User

import os

from lib.helper import user_data_path


class Student(User):
    def __init__(
        self,
        uid: int = -1,
        username: str = "",
        password: str = "",
        register_time: str = "",
        role: str = "",
        email: str = "",
    ):
        super().__init__(uid, username, password, register_time, role)
        self.email = email

    def __str__(self):
        return_str = (
            f"{self.uid};;;{self.username};;;{self.password};;;"
            + f"{self.register_time};;;{self.role},"
            + f"{self.email}"
        )
        return return_str

    @classmethod
    def get_students_by_page(cls, page):
        page = int(page)
        user_path = user_data_path

        total_students = []
        with open(user_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip().strip("\n").split(";;;")
                if len(li) > 5 and li[4] == "student":
                    one_student = Student(
                        int(li[0]),
                        li[1],
                        li[2],
                        li[3],
                        li[4],
                        li[5],
                    )
                    total_students.append(one_student)

                line = r.readline()

        page_num = (len(total_students) // 20) + 1
        # print(len(total_instructors), page_num)

        min_idx = int(page) * 20 - 20
        idx = 0
        return_students = []
        for idx, one_student in enumerate(total_students):
            if idx >= min_idx and idx < min_idx + 20:
                return_students.append(one_student)

        # print(return_instructors)

        return (return_students, page_num, len(total_students))

    @classmethod
    def get_student_by_id(cls, id):
        user_path = user_data_path

        with open(user_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip().strip("\n").split(";;;")
                if len(li) > 5 and li[4] == "student" and str(li[0]) == str(id):
                    one_student = Student(
                        int(li[0]),
                        li[1],
                        li[2],
                        li[3],
                        li[4],
                        li[5],
                    )
                    return one_student
                line = r.readline()

        return None

    @classmethod
    def delete_student_by_id(cls, id):
        user_path = user_data_path
        tmp_path = "tmp_user.txt"

        with open(tmp_path, "w", encoding='utf-8') as w:
            with open(user_path, "r", encoding='utf-8') as r:
                line = r.readline()
                while line:
                    li = line.strip().strip("\n").split(";;;")
                    if len(li) > 5 and li[4] == "student" and str(li[0]) == str(id):
                        pass
                    else:
                        w.write(line)
                    line = r.readline()
        os.remove(user_path)
        os.rename(tmp_path, user_path)
