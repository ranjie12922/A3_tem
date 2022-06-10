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


class Course:

    """
    category_title,subcategory_id,subcategory_title,subcategory_description,
    subcategory_url,course_id,course_title,course_url,num_of_subscribers,
    avg_rating,num_of_reviews
    """

    def __init__(
        self,
        category_title,
        subcategory_id,
        subcategory_title,
        subcategory_description,
        subcategory_url,
        course_id,
        course_title,
        course_url,
        num_of_subscribers,
        avg_rating,
        num_of_reviews,
    ):
        self.category_title = category_title
        self.subcategory_id = subcategory_id
        self.subcategory_title = subcategory_title
        self.subcategory_description = subcategory_description
        self.subcategory_url = subcategory_url
        self.course_id = course_id
        self.course_title = course_title
        self.course_url = course_url
        self.num_of_subscribers = num_of_subscribers
        self.avg_rating = avg_rating
        self.num_of_reviews = num_of_reviews

    def __str__(self):
        return (
            f"{self.category_title};;;{self.subcategory_id};;;"
            + f"{self.course_id};;;{self.course_title};;;"
            + f"{self.course_url};;;{self.num_of_subscribers};;;"
            + f"{self.avg_rating};;;{self.num_of_reviews}"
        )

    @classmethod
    def get_courses(cls):
        path = course_json_files_path
        save_path = course_data_path

        with open(save_path, "w", encoding='utf-8') as w:
            w.write("")

        with open(save_path, "w",encoding="utf-8") as w:
            for sub_file in os.listdir(path):
                # print(subpath)
                category_title = sub_file.split("_")[2]
                # print(category_title)
                sub_path = os.path.join(path, sub_file)
                for sub_sub_file in os.listdir(sub_path):
                    sub_sub_path = os.path.join(sub_path, sub_sub_file)
                    # print(sub_sub_path)
                    for sss_file in os.listdir(sub_sub_path):
                        sss_path = os.path.join(sub_sub_path, sss_file)
                        with open(sss_path, "r", encoding='utf-8') as r:
                            one_course = json.load(r)
                            subcategory_id = sss_file.split(".")[0]

                            sub_info = one_course["unitinfo"]["source_objects"][0]
                            for key in sub_info:
                                if not sub_info[key]:
                                    sub_info[key] = "null"
                            subcategory_title = sub_info["title"]
                            subcategory_description = sub_info["description"]
                            subcategory_url = sub_info["url"]

                            coures_info = one_course["unitinfo"]["items"]
                            for item in coures_info:
                                course_id = item["id"]
                                course_title = item["title"]
                                course_url = item["url"]
                                num_of_subscribers = item["num_subscribers"]
                                avg_rating = item["avg_rating"]
                                num_of_reviews = item["num_reviews"]
                                w.write(
                                    f"{category_title};;;{subcategory_id};;;"
                                    + f"{subcategory_title};;;{subcategory_description};;;"
                                    + f"{subcategory_url};;;{course_id};;;"
                                    + f"{course_title};;;{course_url};;;"
                                    + f"{num_of_subscribers};;;{avg_rating};;;{num_of_reviews}"
                                )
                                w.write("\n")

    @classmethod
    def clear_course_data(cls):
        save_path = course_data_path
        with open(save_path, "w", encoding='utf-8') as w:
            w.write("")

    @classmethod
    def generate_page_num_list(cls, page, total_pages):
        page = int(page)
        total_pages = int(total_pages)
        if page <= 5:
            return range(1, 10)
        if total_pages - 4 > page:
            return range(page - 4, page + 5)
        else:
            return range(total_pages - 8, total_pages + 1)

    @classmethod
    def get_courses_by_page(cls, page):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        page = int(page)
        save_path = course_data_path
        total_num_courses = 0
        with open(save_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip()
                if len(li) > 0:
                    total_num_courses += 1
                line = r.readline()

        page_num = (total_num_courses // 20) + 1

        min_idx = page * 20 - 20
        idx = 0
        courses = []
        with open(save_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip().split(";;;")
                if len(li) == 11:
                    if idx >= min_idx and idx < min_idx + 20:
                        one_course = Course(
                            li[0],
                            li[1],
                            li[2],
                            li[3],
                            li[4],
                            li[5],
                            li[6],
                            li[7],
                            li[8],
                            li[9],
                            li[10],
                        )
                        courses.append(one_course)
                idx += 1
                line = r.readline()

        # print(total_num_courses)

        return (courses, page_num, total_num_courses)

    @classmethod
    def delete_course_by_id(cls, temp_course_id):
        save_path = course_data_path
        tmp_path = "tmp_coures.txt"

        found = False

        with open(tmp_path, "w", encoding='utf-8') as w:
            with open(save_path, "r", encoding='utf-8') as r:
                line = r.readline()
                while line:
                    li = line.strip().strip("\n").split(";;;")
                    if len(li) >= 11 and str(li[5]) == str(temp_course_id):
                        found = True
                    else:
                        w.write(line)
                    line = r.readline()
        os.remove(save_path)
        os.rename(tmp_path, save_path)

        tmp_path2 = "tmp_instructor.txt"
        if not found:
            return found

        with open(tmp_path2, "w", encoding='utf-8') as w:
            with open(user_data_path, "r", encoding='utf-8') as r:
                line = r.readline()
                while line:
                    li = line.strip().strip("\n").split(";;;")
                    if len(li) >= 9 and str(li[4]) == "instructor":
                        course_ids = li[8].strip("\n").split("--")
                        for course in course_ids:
                            try:
                                course = int(course)
                                temp_course_id = int(temp_course_id)
                                if course == temp_course_id:
                                    course_ids.remove(str(course))
                                    print(course_ids)
                            except:
                                pass

                        course_id_li_str = ""
                        for idx, this_id in enumerate(course_ids):
                            if idx == len(course_ids) - 1:
                                course_id_li_str = course_id_li_str + str(this_id)
                            else:
                                course_id_li_str = (
                                    course_id_li_str + str(this_id) + "--"
                                )
                        w.write(
                            f"{li[0]};;;{li[1]};;;{li[2]};;;"
                            + f"{li[3]};;;{li[4]};;;{li[5]};;;"
                            + f"{li[6]};;;"
                            + f"{li[7]};;;{course_id_li_str}"
                        )
                        w.write("\n")

                    else:
                        w.write(line)
                    line = r.readline()
        os.remove(user_data_path)
        os.rename(tmp_path2, user_data_path)

        return found

    @classmethod
    def get_course_by_course_id(cls, temp_course_id):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        path = course_data_path

        one_course = None
        with open(path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip().split(";;;")
                if len(li) > 0:
                    if str(li[5]) == str(temp_course_id):
                        one_course = Course(
                            li[0],
                            li[1],
                            li[2],
                            li[3],
                            li[4],
                            li[5],
                            li[6],
                            li[7],
                            li[8],
                            li[9],
                            li[10],
                        )
                        break
                line = r.readline()
        comment = ""
        if one_course:
            num_subscribers = int(one_course.num_of_subscribers)
            avg_rating = float(one_course.avg_rating)
            num_reviews = int(one_course.num_of_reviews)
            if num_subscribers > 100000 and avg_rating > 4.5 and num_reviews > 10000:
                comment = "Top Courses"
            elif num_subscribers > 50000 and avg_rating > 4.0 and num_reviews > 5000:
                comment = "Popular Courses"
            elif num_subscribers > 10000 and avg_rating > 4.0 and num_reviews > 1000:
                comment = "Good Courses"
            else:
                comment = "General Courses"

        return (one_course, comment)

    @classmethod
    def get_course_by_instructor_id(cls, instructor_id):
        course_objs = []
        # print(instructor_id)

        with open(user_data_path, "r", encoding='utf-8') as user_r:
            line = user_r.readline()
            while line:
                li = line.strip().strip("\n").split(";;;")
                if len(li) > 4:
                    if str(li[0]) == str(instructor_id) and str(li[4]) == "instructor":
                        course_list = li[8].strip("\n").split("--")
                        print(course_list)
                        for course_id in course_list:
                            if course_id != "":
                                one_course, comment = cls.get_course_by_course_id(
                                    course_id
                                )
                                course_objs.append(one_course)
                        break
                line = user_r.readline()
        if len(course_objs) > 20:
            return (course_objs[:20], 20)
        return (course_objs, len(course_objs))

    @classmethod
    def generate_course_figure1(cls):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        df = cls.all_course_to_df()
        this_choose = df.groupby("subcategory_title")["num_of_subscribers"].sum()
        order_s = this_choose.sort_values(0, ascending=False)
        index = order_s.index.values.tolist()
        val = order_s.values.tolist()

        fig = plt.figure(figsize=(10, 13))
        plt.bar(index[:10], val[:10])
        # plt.tight_layout()
        plt.xticks(rotation=70)

        save_path = figure_save_path + "course_figure1.png"
        plt.savefig(save_path)

        return_str = "top10 subcategory: "
        for name in index[:10]:
            return_str = return_str + name + ","

        return return_str[: len(return_str) - 1]

    @classmethod
    def generate_course_figure2(cls):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        df = cls.all_course_to_df()
        df1 = df[df["num_of_reviews"] > 50000]
        df2 = df1.sort_values(by=["avg_rating"], ascending=False)

        course = df2["course_title"].tolist()
        rating = df2["avg_rating"].tolist()

        for i, c in enumerate(course):
            if len(c) > 30:
                li = course[i].split(" ")
                if len(li) >= 3:
                    course[i] = li[0] + " " + li[1] + " " + li[2] + " "
                else:
                    tmp_str = ""
                    for item in li:
                        tmp_str = tmp_str + item + " "
                    tmp_str = tmp_str[: len(tmp_str) - 1]
                    course[i] = tmp_str

        fig = plt.figure(figsize=(10, 13))
        plt.bar(course[:10], rating[:10])
        # plt.tight_layout()
        plt.xticks(rotation=70)

        save_path = figure_save_path + "course_figure2.png"
        plt.savefig(save_path)

        return_str = "top10 course: "
        for name in course[:10]:
            return_str = return_str + name + ","

        return return_str[: len(return_str) - 1]

    @classmethod
    def generate_course_figure3(cls):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        df = cls.all_course_to_df()
        df1 = df[10000 <= df["num_of_subscribers"]]
        df2 = df1[df1["num_of_subscribers"] <= 100000]

        subscribers = df2["num_of_subscribers"].tolist()
        rating = df2["avg_rating"].tolist()

        fig = plt.figure(figsize=(12, 10))
        plt.scatter(subscribers, rating)
        # plt.tight_layout()
        # plt.xticks(rotation=70)

        save_path = figure_save_path + "course_figure3.png"
        plt.savefig(save_path)

        return "found {} points".format(len(subscribers))

    @classmethod
    def generate_course_figure4(cls):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        df = cls.all_course_to_df()
        subscribers_num = df.groupby("category_title")["num_of_subscribers"].sum()

        labels = subscribers_num.index.values.tolist()
        val = subscribers_num.values.tolist()

        fig = plt.figure(figsize=(12, 10))
        plt.pie(val, labels=labels)
        # plt.tight_layout()
        # plt.xticks(rotation=70)

        save_path = figure_save_path + "course_figure4.png"
        plt.savefig(save_path)

        return_str = "category subscribers: "
        for i, v in enumerate(val):
            return_str = return_str + labels[i] + "/" + str(v) + " "
        return return_str[0 : len(return_str) - 1]

    @classmethod
    def generate_course_figure5(cls):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        df = cls.all_course_to_df()
        no_reviews = df[df["num_of_reviews"] == 0]
        have_reviews = df[df["num_of_reviews"] != 0]

        print(len(no_reviews))
        print(len(have_reviews))

        fig = plt.figure(figsize=(10, 9))
        plt.bar(["no_reviews", "have_reviews"], [len(no_reviews), len(have_reviews)])
        # plt.tight_layout()
        plt.xticks(rotation=70)

        save_path = figure_save_path + "course_figure5.png"
        plt.savefig(save_path)

        return "no_reviews:{} have_reviews:{}".format(
            len(no_reviews), len(have_reviews)
        )

    @classmethod
    def generate_course_figure6(cls):
        """
        category_title,subcategory_id,subcategory_title,subcategory_description,
        subcategory_url,course_id,course_title,course_url,num_of_subscribers,
        avg_rating,num_of_reviews
        """
        df = cls.all_course_to_df()
        course_num = df.groupby("subcategory_title")["course_id"].count()
        order_course_num = course_num.sort_values(0)

        labels = order_course_num.index.values.tolist()
        val = order_course_num.values.tolist()

        fig = plt.figure(figsize=(12, 12))
        plt.bar(labels[:10], val[:10])
        # plt.tight_layout()
        plt.xticks(rotation=70)

        save_path = figure_save_path + "course_figure6.png"
        plt.savefig(save_path)

        return_str = "top10 course num of subcategory: "
        for i, v in enumerate(val[:10]):
            return_str = return_str + labels[i] + "/" + str(v) + " "
        return return_str[0 : len(return_str) - 1]

    @classmethod
    def all_course_to_df(cls):
        all_list = []
        with open(course_data_path, "r", encoding='utf-8') as r:
            line = r.readline()
            while line:
                li = line.strip().strip("\n").split(";;;")
                if len(li) >= 11:
                    all_list.append(li)
                line = r.readline()

        df = pd.DataFrame(
            all_list,
            columns=[
                "category_title",
                "subcategory_id",
                "subcategory_title",
                "subcategory_description",
                "subcategory_url",
                "course_id",
                "course_title",
                "course_url",
                "num_of_subscribers",
                "avg_rating",
                "num_of_reviews",
            ],
        )

        df = df.astype(
            {"num_of_subscribers": int, "avg_rating": float, "num_of_reviews": int}
        )

        # print(df.dtypes)
        # print(df.head())

        return df


if __name__ == "__main__":
    # Course.get_courses()
    courses, page, total = Course.get_courses_by_page(2)
    for course in courses:
        print(course.__str__())
