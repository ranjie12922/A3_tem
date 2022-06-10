from flask import Blueprint, render_template, request, url_for, redirect
from lib.helper import (
    render_result,
    render_err_result,
)
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)


def generate_user(login_user_str):
    li = login_user_str.strip().strip("\n").split(";;;")
    if len(li) < 5:
        return

    User.current_login_user = None
    if li[4] == "admin":
        User.current_login_user = Admin(int(li[0]), li[1], li[2], li[3], li[4])
    elif li[4] == "student":
        User.current_login_user = Student(int(li[0]), li[1], li[2], li[3], li[4], li[5])
    elif li[4] == "instructor":
        course_id_list = li[8].strip("\n").split("--")
        User.current_login_user = Instructor(
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
    # print(User.current_login_user.__str__())


@user_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("00login.html")
    elif request.method == "POST":
        code, msg = login_post(request)
        if code != 200:
            return render_err_result(code=code, msg=msg)
        else:
            return render_result(code=code, msg=msg)


def login_post(request):
    username = request.values["username"]
    password = request.values["password"]

    if not (User.validate_username(username) and User.validate_password(password)):
        return (-1, "username or password is wrong")

    user_str = User.authenticate_user(username, password)
    if not user_str:
        return (-1, "can not find this user")
    else:
        generate_user(user_str)
        return (200, "login success")


@user_page.route("/logout")
def logout():
    User.current_login_user = None
    return render_template("01index.html")


@user_page.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("00register.html")
    elif request.method == "POST":
        code, msg = register_post(request)
        if code == 200:
            return render_result(code=code, msg=msg)
        else:
            return render_err_result(code=code, msg=msg)


def register_post(request):
    username = request.values["username"]
    password = request.values["password"]
    email = request.values["email"]
    register_time = request.values["register_time"]
    role = request.values["role"]

    print(User.validate_username(username))
    print(User.validate_password(password))
    print(User.validate_email(email))

    if not (
        User.validate_username(username)
        and User.validate_password(password)
        and User.validate_email(email)
    ):
        return (-1, "proper message for users")

    if User.check_username_exist(username):
        return (-1, "username has found in system!")

    User.register_user(username, password, register_time, role, email)
    return (200, "success")


@user_page.route("/student-list")
def student_list():
    """
    “context['one_page_user_list']”,
    “context['total_pages']”, “context['page_num_list']”, “context['current_page']”,
    “context['total_num']”, “context["current_user_role"]”
    """
    if User.current_login_user:
        if "page" in request.args.keys():
            page = request.args["page"]
        else:
            page = 1

        (
            one_page_user_list,
            total_pages,
            total_num,
        ) = Student.get_students_by_page(page)
        if User.current_login_user:
            current_user_role = User.current_login_user.role
        else:
            current_user_role = ""

        page_num_list = Course.generate_page_num_list(page, total_pages)

    else:
        return redirect(url_for("index_page.index"))
    return render_template(
        "10student_list.html",
        one_page_user_list=one_page_user_list,
        current_page=int(page),
        total_num=total_num,
        current_user_role=current_user_role,
        total_pages=total_pages,
        page_num_list=page_num_list,
    )


@user_page.route("/student-info")
def student_info():
    if "id" in request.args.keys():
        id = request.args["id"]
    else:
        id = User.current_login_user.uid

    student = Student.get_student_by_id(id)
    if student:
        user = student
    else:
        user = User.current_login_user
    if User.current_login_user:
        role = User.current_login_user.role
    else:
        role = ""
    return render_template("11student_info.html", user=user, current_user_role=role)


@user_page.route("/student-delete")
def student_delete():
    id = request.args["id"]
    Student.delete_student_by_id(id)
    return url_for("user_page.student-list", page=1)
