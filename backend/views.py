import json

from io import StringIO
from xlwt import *
from django.views.decorators.http import require_POST, require_GET
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse

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
                    "token": generate_token(id, 'student'),
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
                    "token": generate_token(id, "teacher"),
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
                    "token": generate_token(id, "admin"),
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


def get_user_info(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'student':
            student = Student.objects.get(id=data['id'])
            return APIResult({
                "name": student.name,
                "id": student.id,
                "gender": "男" if not student.gender else "女",
                "grade": student.grade,
                "college": student.college,
                "subject": student.subject,
                "class_name": student.class_name,
                # 待补充头像不存在的情况
                "avatar": "http://localhost:8001" + student.avatar.url
            })
        elif data['type'] == 'teacher':
            teacher = Teacher.objects.get(id=data['id'])
            return APIResult({
                "name": teacher.name,
                "id": teacher.id,
                "gender": "男" if not teacher.gender else "女",
                "college": teacher.college,
                "institute": teacher.institute,
                "subject": teacher.subject,
                "avatar": "http://localhost:8001" + teacher.avatar.url
            })
    else:
        return APIServerError("error")


def update_password(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    old_pass = request_post['oldPass']
    new_pass = request_post['pass']
    data = check_token(token)
    if data['res']:
        user_type = data['type']
        if user_type == 'student':
            student = Student.objects.get(id=data['id'])
            if validate_password(student.password, old_pass):
                student.password = encrypt_password(new_pass)
                student.save()
                return APIResult({
                    'result': True,
                    'message': '修改密码成功',
                    'type': 'student'
                })
            else:
                return APIResult({
                    'result': False,
                    'message': '密码错误'
                })
        elif user_type == 'teacher':
            teacher = Teacher.objects.get(id=data['id'])
            if validate_password(teacher.password, old_pass):
                teacher.password = encrypt_password(new_pass)
                teacher.save()
                return APIResult({
                    'result': True,
                    'message': '修改密码成功',
                    'type': 'teacher'
                })
            else:
                return APIResult({
                    'result': False,
                    'message': '密码错误'
                })
    else:
        return APIServerError("error")


def get_student_resume(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        student = Student.objects.get(id=data['id'])
        return APIResult({
            "id": student.id,
            "gpa": student.gpa,
            "rank": student.rank,
            "profile": student.profile,
            "award": student.award,
            "agreeDistribution": student.agree_distribution,
            # 待补充头像不存在的情况
            "avatar": "http://localhost:8001" + student.avatar.url
        })
    else:
        return APIServerError("error")


def update_resume(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    form = request_post['form']
    data = check_token(token)
    if data['res']:
        student = Student.objects.get(id=data['id'])
        student.gpa = form['gpa']
        student.rank = form['rank']
        student.agree_distribution = form['agreeDistribution']
        student.profile = form['profile']
        student.award = form['award']
        student.save()
        return APIResult({
            'result': True,
            'message': '修改简历成功'
        })
    else:
        return APIResult({
            'result': False,
            'message': '修改简历错误'
        })


def get_teachers(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    if 'select' in request_post:
        select = request_post['select']
    else:
        select = None
    data = check_token(token)
    if data['res']:
        res = ["", ""]
        ids = []
        teachers_res = []
        if not select:
            selections = Selection.objects.filter(student_id=data['id'])
            for selection in selections:
                ids.append(selection.teacher.id)
                if selection.is_first:
                    res[0] = selection.teacher.id
                    teachers_res.insert(0, {
                        "id": selection.teacher.id,
                        "name": selection.teacher.name,
                        "college": selection.teacher.college,
                        "institute": selection.teacher.institute,
                        "subject": selection.teacher.subject,
                        "profile": selection.teacher.profile
                    })
                else:
                    res[1] = selection.teacher.id
                    teachers_res.append({
                        "id": selection.teacher.id,
                        "name": selection.teacher.name,
                        "college": selection.teacher.college,
                        "institute": selection.teacher.institute,
                        "subject": selection.teacher.subject,
                        "profile": selection.teacher.profile
                    })
        else:
            for i, j in enumerate(select):
                if j:
                    teacher = Teacher.objects.get(id=j)
                    res[i] = teacher.id
                    teachers_res.append({
                        "id": teacher.id,
                        "name": teacher.name,
                        "college": teacher.college,
                        "institute": teacher.institute,
                        "subject": teacher.subject,
                        "profile": teacher.profile
                    })
                    ids = select
        teachers = Teacher.objects.all()
        for teacher in teachers:
            if teacher.id not in ids:
                teachers_res.append({
                    "id": teacher.id,
                    "name": teacher.name,
                    "college": teacher.college,
                    "institute": teacher.institute,
                    "subject": teacher.subject,
                    "profile": teacher.profile
                })
        return APIResult({
            "teachers": teachers_res,
            "select": res,
            "options": Teacher.get_institute_list()
        })
    return APIServerError({"message": data['message']})


def get_teachers_by_institute(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    institutes = request_post['institutes']
    select = request_post['select']
    data = check_token(token)
    if data['res']:
        teachers = Teacher.objects.filter(institute__in=institutes)
        teachers_res = []
        for i in select:
            if i:
                teacher = Teacher.objects.get(id=i)
                teachers_res.append({
                    "id": teacher.id,
                    "name": teacher.name,
                    "college": teacher.college,
                    "institute": teacher.institute,
                    "subject": teacher.subject,
                    "profile": teacher.profile
                })
        for teacher in teachers:
            if teacher.id not in select:
                teachers_res.append({
                    "id": teacher.id,
                    "name": teacher.name,
                    "college": teacher.college,
                    "institute": teacher.institute,
                    "subject": teacher.subject,
                    "profile": teacher.profile
                })
        return APIResult({
            "teachers": teachers_res
        })
    return APIServerError({"message": data['message']})


def update_selection(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    select = request_post['select']
    data = check_token(token)
    if data['res']:
        if select[0]:
            selection = Selection.objects.filter(student_id=data['id'], is_first=True)
            if selection:
                selection = selection.first()
                selection.teacher = Teacher.objects.get(id=select[0])
                selection.save()
            else:
                Selection.objects.create(student=Student.objects.get(id=data['id']),
                                         teacher=Teacher.objects.get(id=select[0]),
                                         is_first=True)
        if select[1]:
            selection = Selection.objects.filter(student_id=data['id'], is_first=False)
            if selection:
                selection = selection.first()
                selection.teacher = Teacher.objects.get(id=select[1])
                selection.save()
            else:
                Selection.objects.create(student=Student.objects.get(id=data['id']),
                                         teacher=Teacher.objects.get(id=select[1]),
                                         is_first=False)
        return APIResult({
            "result": True,
            "message": "修改成功"
        })
    return APIServerError({"message": data['message']})


def get_selection_result(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        selections = Selection.objects.filter(student_id=data['id'])
        res = []
        for selection in selections:
            if selection.is_first:
                res.insert(0, {
                    "type": "第一志愿",
                    "name": selection.teacher.name,
                    "college": selection.teacher.college,
                    "institute": selection.teacher.institute,
                    "subject": selection.teacher.subject,
                    "profile": selection.teacher.profile,
                    "pass_status": selection.pass_status
                })
            else:
                res.append({
                    "type": "第二志愿",
                    "name": selection.teacher.name,
                    "college": selection.teacher.college,
                    "institute": selection.teacher.institute,
                    "subject": selection.teacher.subject,
                    "profile": selection.teacher.profile,
                    "pass_status": selection.pass_status
                })
        return APIResult(res)
    return APIServerError({"message": data['message']})


def get_announcement(request):
    pass


def export_excel(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        selections = Selection.objects.filter(teacher_id=data['id'])
        if selections:
            excel = Workbook(encoding='utf-8')
            sheet = excel.add_sheet('本科学生列表')
            header = ['学号', '姓名', '性别', '年级', '学院', '专业', '班级', '绩点', '绩点排名', '个人简介', '获奖情况', '志愿']
            for index, value in enumerate(header):
                sheet.write(0, index, value)
            row = 1
            for selection in selections:
                student = selection.student
                excel_data = [
                    student.id,
                    student.name,
                    "男" if not student.gender else "女",
                    student.grade,
                    student.college,
                    student.subject,
                    student.class_name,
                    student.gpa,
                    student.rank,
                    student.profile,
                    student.award,
                    "第一志愿" if selection.is_first else "第二志愿"
                ]
                for index, value in enumerate(excel_data):
                    sheet.write(row, index, value)
                row += 1
            output = StringIO()
            excel.save(output)
            output.seek(0)
            response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=学生选择信息表.xls'
            response.write(output.getvalue())
            return response
    return HttpResponse("无数据")


def check_token(token):
    data = certify_token(token)
    if 'id' in data:
        return {
            "res": True,
            "id": data["id"],
            "type": data["type"]
        }
    else:
        return {
            "res": False,
            "message": data
        }
