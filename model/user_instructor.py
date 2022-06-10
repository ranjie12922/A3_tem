# coding=utf-8
from model.user import User
import os
import json

import pandas as pd
import matplotlib.pyplot as plt

from lib.helper import (
    course_data_path,
    user_data_path,
    course_json_files_path,
    figure_save_path,
)


class Instructor(User):
    def __init__(
        self,
        uid: int,
        username: str,
        password: str,
        register_time: str,
        role: str,
        email: str,
        display_name: str,
        job_title: str,
        course_id_list,
    ):
        super().__init__(uid, username, password, register_time, role)
        self.email = email
        self.display_name = display_name
        self.job_title = job_title
        self.course_id_list = course_id_list

    def __str__(self):
        """
        “{instructor_id};;;{username};;;{password};;;{register_time};;;{role};;;{email};;;{
        instructor_display_name};;;{instructor_job_title};;;{course_id_list}”.
        """
        return_str = (
            f"{self.uid};;;{self.username};;;{self.password};;;"
            + f"{self.register_time};;;{self.role},"
            + f"{self.email};;;{self.display_name}"
            + f"{self.job_title};;;{self.course_id_list}"
        )
        return return_str

    @classmethod
    def get_instructors(cls):
        path = course_json_files_path
        save_path = user_data_path
        tmp_path = "tmp_user.txt"
        tmp2_path = "tmp2_user.txt"

        tmp_instructors = {}

        # 循环第一层
        for sub_file in os.listdir(path):
            # print(subpath)
            # print(category_title)
            sub_path = os.path.join(path, sub_file)
            # 循环第二层
            for sub_sub_file in os.listdir(sub_path):
                sub_sub_path = os.path.join(sub_path, sub_sub_file)
                # print(sub_sub_path)
                # 循环最后一次，json文件
                for sss_file in os.listdir(sub_sub_path):
                    sss_path = os.path.join(sub_sub_path, sss_file)
                    # 打开json
                    with open(sss_path, "r", encoding='utf-8') as r:
                        # 载入为dict
                        one_course = json.load(r)
                        coures_info = one_course["unitinfo"]["items"]
                        for item in coures_info:
                            """
                            “{instructor_id};;;{username};;;{password};;;{register_time};;;
                            {role};;;{email};;;{instructor_display_name};;;
                            {instructor_job_title};;;{course_id_list}”.
                            """
                            instructor_info = item["visible_instructors"]

                            # 获取instructor信息,写入临时文件
                            for instructor in instructor_info:
                                instructor_id = instructor["id"]

                                username = (
                                    instructor["display_name"]
                                    .strip()
                                    .lower()
                                    .replace(" ", "_")
                                )
                                password = User.encrypt_password(instructor["id"])
                                register_time = "xx-xx-xxxx"
                                role = "instructor"
                                email = username + "@gmail.com"
                                display_name = instructor["display_name"]
                                job_title = instructor["job_title"]
                                course_id = item["id"]
                                course_id_li = [course_id]

                                li = [
                                    instructor_id,
                                    username,
                                    password,
                                    register_time,
                                    role,
                                    email,
                                    display_name,
                                    job_title,
                                    course_id_li,
                                ]

                                if instructor_id not in tmp_instructors.keys():
                                    tmp_instructors[instructor_id] = li
                                else:
                                    if (
                                        course_id
                                        not in tmp_instructors[instructor_id][8]
                                    ):
                                        tmp_instructors[instructor_id][8].append(
                                            course_id
                                        )

        with open(tmp_path, "w", encoding='utf-8') as w:
            for k, v in tmp_instructors.items():
                courses_li_str = ""
                courses = v[8]
                for i, course in enumerate(courses):
                    if i < len(courses) - 1:
                        courses_li_str = courses_li_str + str(course) + "--"
                    else:
                        courses_li_str = courses_li_str + str(course)
                w.write(
                    f"{v[0]};;;"
                    + f"{v[1]};;;"
                    + f"{v[2]};;;"
                    + f"{v[3]};;;"
                    + f"{v[4]};;;"
                    + f"{v[5]};;;"
                    + f"{v[6]};;;"
                    + f"{v[7]};;;"
                    + f"{courses_li_str}"
                )
                w.write("\n")

        with open(user_data_path, "r", encoding='utf-8') as r:
            with open(tmp2_path, "w", encoding='utf-8') as w:
                line = r.readline()
                while line:
                    li = line.strip().strip("\n").split(";;;")
                    if len(li) >= 9 and li[3] == "xx-xx-xxxx" and li[4] == "instructor":
                        pass
                    else:
                        w.write(line)
                    line = r.readline()

        with open(tmp_path, "r", encoding='utf-8') as r:
            with open(tmp2_path, "a", encoding='utf-8') as w:
                line = r.readline()
                while line:
                    w.write(line)
                    line = r.readline()

        os.remove(tmp_path)
        os.remove(user_data_path)
        os.rename(tmp2_path, user_data_path)

    @classmethod
    def get_instructors_by_page(cls, page):
        page = int(page)
        user_path = user_data_path

        total_instructors = []
        with open(user_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip().strip("\n").split(";;;")
                if len(li) >= 9 and li[4] == "instructor":
                    course_id_list = li[8].strip("\n").split("--")
                    one_instructor = Instructor(
                        int(li[0]),
                        li[1],
                        li[2],
                        li[3],
                        li[4],
                        li[5],
                        li[6],
                        li[7],
                        course_id_list,
                    )
                    total_instructors.append(one_instructor)
                line = r.readline()

        page_num = (len(total_instructors) // 20) + 1
        # print(len(total_instructors), page_num)

        min_idx = page * 20 - 20
        idx = 0
        return_instructors = []
        for idx, one_instructor in enumerate(total_instructors):
            if idx >= min_idx and idx < min_idx + 20:
                return_instructors.append(total_instructors[idx])

        # print(return_instructors)

        return (return_instructors, page_num, len(total_instructors))

    @classmethod
    def generate_instructor_figure1(cls):
        user_path = user_data_path

        total_instructors = []
        with open(user_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip().strip("\n").split(";;;")
                if len(li) >= 9 and li[4] == "instructor":
                    course_id_list = li[8].strip("\n").split("--")
                    one_li = [
                        int(li[0]),
                        li[1],
                        li[2],
                        li[3],
                        li[4],
                        li[5],
                        li[6],
                        li[7],
                        len(course_id_list),
                    ]

                    total_instructors.append(one_li)
                line = r.readline()

        cols = [
            "uid",
            "username",
            "password",
            "register_time",
            "role",
            "email",
            "display_name",
            "job_title",
            "course_id_list",
        ]

        df = pd.DataFrame(total_instructors, columns=cols)
        df1 = df.sort_values("course_id_list", ascending=False)

        labels = df1["username"].tolist()
        val = df1["course_id_list"].tolist()

        fig = plt.figure(figsize=(10, 13))
        plt.bar(labels[:10], val[:10])
        # plt.tight_layout()
        plt.xticks(rotation=70)

        save_path = figure_save_path + "instructor_figure1.png"
        plt.savefig(save_path)

        return_str = "top10 instructors: "

        for i, item in enumerate(val[:10]):
            return_str = return_str + labels[i] + "/" + str(item) + " "
        return return_str[: len(return_str) - 1]


if __name__ == "__main__":
    # User.clear_user_data()
    # Instructor.get_instructors()
    Instructor.get_instructors_by_page(2)
