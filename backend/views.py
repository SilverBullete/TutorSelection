import json

from django.views.decorators.http import require_POST, require_GET
from django.db.models import ObjectDoesNotExist

from .models import Student, Teacher, Administrator, Selection, Publicity, OpeningTime, File
from .response import APIResult, APIServerError
from .encryption import encrypt_password, certify_token, generate_token, validate_password


@require_POST
def login(request):
    request_post = json.loads(request.body)
    account_type = request_post['type']
    id = request_post['id']
    password = request_post['password']
    if account_type == "学生":
        try:
            student = Student.objects.get(id=id)
            if validate_password(student.password, password):
                return APIResult({
                    "token": generate_token(id),
                    "type": "student"
                })
            return APIServerError("密码错误")
        except ObjectDoesNotExist:
            return APIServerError("用户名不存在")
    elif account_type == "教师":
        try:
            teacher = Teacher.objects.get(id=id)
            if validate_password(teacher.password, password):
                return APIResult({
                    "token": generate_token(id),
                    "type": "teacher"
                })
            return APIServerError("密码错误")
        except ObjectDoesNotExist:
            return APIServerError("用户名不存在")
    elif account_type == "管理员":
        try:
            admin = Administrator.objects.get(username=id)
            if validate_password(admin.password, password):
                return APIResult({
                    "token": generate_token(id),
                    "type": "admin"
                })
            return APIServerError("密码错误")
        except ObjectDoesNotExist:
            return APIServerError("用户名不存在")


def create(request):
    # print(encrypt_password("123456"))
    # Student.objects.create(id="201700000000", password=encrypt_password("123456"))
    # Teacher.objects.create(id="000000000000", password=encrypt_password("123456"))
    # Administrator.objects.create(username="admin", password=encrypt_password("123456"))
    return APIResult({}, "添加成功")
