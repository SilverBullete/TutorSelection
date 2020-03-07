import json
import datetime
import time

from io import BytesIO
from xlwt import *
from django.views.decorators.http import require_POST
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.http import urlquote

from .models import Student, Teacher, Administrator, Selection, Publicity, OpeningTime, Institute
from .response import APIResult, APIServerError
from .encryption import encrypt_password, certify_token, generate_token, validate_password
from TutorSelection.settings import MEDIA_ROOT

MAX_NUM = 8
PASSING = 0
PENDING = 1
NOT_PASSING = 2
PASS_STATUS = ['通过', '待通过', '未通过']


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
    else:
        return APIServerError('error')


def get_user_type(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        return APIResult({
            "type": data['type']
        })
    return APIServerError(data['message'])


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
                "avatar": "http://localhost:8001" + student.avatar.url,
                "phone": student.phone,
                "email": student.email
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
            return APIServerError('error')
    return APIServerError(data['message'])


def update_user_info(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    form = request_post['form']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'student':
            student = Student.objects.get(id=data['id'])
            student.phone = form['phone']
            student.email = form['email']
            student.save()
            return APIResult({
                'result': True,
                'message': '修改成功',
                'type': 'student'
            })
        elif data['type'] == 'teacher':
            teacher = Teacher.objects.get(id=data['id'])
            teacher.subject = form['subject']
            teacher.save()
            return APIResult({
                'result': True,
                'message': '修改成功',
                'type': 'teacher'
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


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
        elif user_type == 'admin':
            admin = Administrator.objects.get(username=data['id'])
            if validate_password(admin.password, old_pass):
                admin.password = encrypt_password(new_pass)
                admin.save()
                return APIResult({
                    'result': True,
                    'message': '修改密码成功',
                    'type': 'admin'
                })
            else:
                return APIResult({
                    'result': False,
                    'message': '密码错误'
                })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


def get_resume(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'student':
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
        elif data['type'] == 'teacher':
            teacher = Teacher.objects.get(id=data['id'])
            return APIResult({
                "id": teacher.id,
                "profile": teacher.profile
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


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
    return APIServerError(data['message'])


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
    return APIServerError(data['message'])


def get_institute_info(request):
    request_post = json.loads(request.body)
    name = request_post['institute']
    institute = Institute.objects.filter(name=name)
    if institute:
        return APIResult({
            "info": institute.first().introduction
        })
    return APIServerError('error')


def update_selection(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    select = request_post['select']
    data = check_token(token)
    if data['res']:
        status, message = is_in_time(data)
        if not status:
            return APIServerError(message)
        if Student.objects.get(id=data['id']).get_tutor() != "暂无":
            return APIServerError("你已经被导师录取，无法继续选择！")
        if select[0]:
            selection = Selection.objects.filter(student_id=data['id'], is_first=True)
            if selection:
                selection = selection.first()
                selection.teacher = Teacher.objects.get(id=select[0])
                selection.save()
            else:
                student = Student.objects.get(id=data['id'])
                Selection.objects.create(student=student,
                                         teacher=Teacher.objects.get(id=select[0]),
                                         is_first=True, round=student.get_round())
        if select[1]:
            selection = Selection.objects.filter(student_id=data['id'], is_first=False)
            if selection:
                selection = selection.first()
                selection.teacher = Teacher.objects.get(id=select[1])
                selection.save()
            else:
                student = Student.objects.get(id=data['id'])
                Selection.objects.create(student=student,
                                         teacher=Teacher.objects.get(id=select[1]),
                                         is_first=False, round=student.get_round())
        return APIResult({
            "result": True,
            "message": "修改成功"
        })
    return APIServerError(data['message'])


def get_selection_result(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'student':
            student = Student.objects.get(id=data['id'])
            selections = Selection.objects.filter(student_id=data['id'], round=student.get_round())
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

            return APIResult({
                'selections': res,
                'teacher': student.get_tutor()
            })
        elif data['type'] == 'teacher':
            selections = Selection.objects.filter(teacher_id=data['id'], pass_status=PASSING)
            res = []
            for selection in selections:
                student = selection.student
                res.append({
                    "id": student.id,
                    "name": student.name,
                    "college": student.college,
                    "subject": student.subject,
                    "class_name": student.class_name,
                    "gpa": student.gpa,
                    "profile": student.profile,
                    "award": student.award,
                    "type": selection.is_first,
                    "avatar": "http://localhost:8001" + student.avatar.url,
                    "pass_status": selection.pass_status
                })
            return APIResult(res)
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


def get_round_time(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            admin = Administrator.objects.get(username=data['id'])
            opening_time = OpeningTime.objects.filter(grade=admin.grade).order_by('-s_end_time')
            if opening_time:
                opening_time = opening_time.first()
                return APIResult({
                    "date": [opening_time.s_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                             opening_time.s_end_time.strftime('%Y-%m-%d %H:%M:%S')]
                })
            return APIServerError('请先开放选择')
        return APIServerError('error')
    return APIServerError(data['message'])


def get_announcement(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'student':
            res = []
            student = Student.objects.get(id=data['id'])
            publicities = Publicity.objects.filter(grade=student.grade).order_by('-end_time')[:5]
            for publicity in publicities:
                res.append({
                    "title": publicity.title,
                    "content": eval(publicity.content),
                    "type": publicity.publicity_type,
                    "start_time": publicity.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "end_time": publicity.end_time.strftime('%Y-%m-%d %H:%M:%S')
                })
            return APIResult({
                "announcements": res
            })
        elif data['type'] == 'teacher':
            res = []
            publicities = Publicity.objects.all().order_by('-end_time')[:5]
            for publicity in publicities:
                res.append({
                    "title": publicity.title,
                    "content": eval(publicity.content),
                    "type": publicity.publicity_type,
                    "start_time": publicity.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "end_time": publicity.end_time.strftime('%Y-%m-%d %H:%M:%S')
                })
            return APIResult({
                "announcements": res
            })
        elif data['type'] == 'admin':
            res = []
            admin = Administrator.objects.get(username=data['id'])
            publicities = Publicity.objects.filter(grade=admin.grade).order_by('-end_time')[:5]
            for publicity in publicities:
                res.append({
                    "title": publicity.title,
                    "content": eval(publicity.content),
                    "type": publicity.publicity_type,
                    "start_time": publicity.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "end_time": publicity.end_time.strftime('%Y-%m-%d %H:%M:%S')
                })
            return APIResult({
                "announcements": res
            })
        return APIServerError('error')
    return APIServerError(data['message'])


def submit_announcement(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    form = request_post['form']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            admin = Administrator.objects.get(username=data['id'])
            content = str(form['content'].strip("").replace(u'\u3000', u' ').split("\n"))
            if form['type'] == 2:
                Publicity.objects.create(grade=admin.grade, title=form['title'],
                                         admin=admin, publicity_type=int(form['type']),
                                         content=content)
            else:
                Publicity.objects.create(grade=admin.grade, title=form['title'],
                                         admin=admin, publicity_type=int(form['type']), content=content,
                                         start_time=datetime.datetime.strptime(form['date'][0], "%Y-%m-%d %H:%M:%S"),
                                         end_time=datetime.datetime.strptime(form['date'][1], "%Y-%m-%d %H:%M:%S"))
            return APIResult({
                "result": True
            })
        return APIServerError('error')
    return APIServerError(data['message'])


def upload_resume(request):
    pdf = request.FILES['file']
    ext = pdf.name.split(".")[-1]
    token = request.POST['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'teacher':
            file_name = '{0}/resume/{1}.{2}'.format(MEDIA_ROOT, data['id'], ext)
            with open(file_name, 'wb') as f:
                for file in pdf.chunks():
                    f.write(file)
            teacher = Teacher.objects.get(id=data['id'])
            teacher.profile = "http://localhost:8001/media/resume/{0}.{1}".format(data['id'], ext)
            teacher.save()
        return APIResult({
            "result": True,
            "message": "上传成功",
            "resume": "http://localhost:8001/media/resume/{0}.{1}".format(data['id'], ext)
        })
    return APIServerError(data['message'])


def get_students(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'teacher':
            student_res = []
            selections = Selection.objects.filter(teacher_id=data['id'], pass_status=PENDING)
            for selection in selections:
                student = selection.student
                student_res.append({
                    "id": student.id,
                    "name": student.name,
                    "college": student.college,
                    "subject": student.subject,
                    "gpa": student.gpa,
                    "rank": student.rank,
                    "profile": student.profile,
                    "award": student.award,
                    "type": selection.is_first,
                    "passStatus": selection.pass_status,
                    "avatar": "http://localhost:8001" + student.avatar.url,
                    "phone": student.phone,
                    "email": student.email,
                    "agree_distribution": "是" if student.agree_distribution else "否"
                })
            return APIResult({
                "students": student_res,
                "maxNum": MAX_NUM
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


def update_students_list(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    select = request_post['select']
    un_select = request_post['unSelect']
    data = check_token(token)
    if data['res']:
        student_res = []
        for i in select:
            student = Student.objects.get(id=i)
            selection = Selection.objects.get(student_id=i, teacher_id=data['id'])
            student_res.append({
                "id": student.id,
                "name": student.name,
                "college": student.college,
                "subject": student.subject,
                "gpa": student.gpa,
                "rank": student.rank,
                "profile": student.profile,
                "award": student.award,
                "type": selection.is_first,
                "passStatus": selection.pass_status,
                "avatar": "http://localhost:8001" + student.avatar.url,
                "phone": student.phone,
                "email": student.email,
                "agree_distribution": "是" if student.agree_distribution else "否"
            })
        selections = Selection.objects.filter(teacher_id=data['id'], pass_status=PENDING)
        for selection in selections:
            student = selection.student
            if student.id not in select + un_select:
                student_res.append({
                    "id": student.id,
                    "name": student.name,
                    "college": student.college,
                    "subject": student.subject,
                    "gpa": student.gpa,
                    "rank": student.rank,
                    "profile": student.profile,
                    "award": student.award,
                    "type": selection.is_first,
                    "passStatus": selection.pass_status,
                    "avatar": "http://localhost:8001" + student.avatar.url,
                    "phone": student.phone,
                    "email": student.email,
                    "agree_distribution": "是" if student.agree_distribution else "否"
                })
        for i in un_select:
            student = Student.objects.get(id=i)
            selection = Selection.objects.get(student_id=i, teacher_id=data['id'])
            student_res.append({
                "id": student.id,
                "name": student.name,
                "college": student.college,
                "subject": student.subject,
                "gpa": student.gpa,
                "rank": student.rank,
                "profile": student.profile,
                "award": student.award,
                "type": selection.is_first,
                "passStatus": selection.pass_status,
                "phone": student.phone,
                "email": student.email,
                "agree_distribution": "是" if student.agree_distribution else "否"
            })
        return APIResult({
            "select": select,
            "unSelect": un_select,
            "students": student_res
        })
    return APIServerError(data['message'])


def submit_selections(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    select = request_post['select']
    unselect = request_post['unSelect']
    data = check_token(token)
    if data['res']:
        for sid in select:
            selection = Selection.objects.filter(teacher_id=data['id'], student_id=sid).first()
            selection.pass_status = PASSING
            selection.save()
        for sid in unselect:
            selection = Selection.objects.filter(teacher_id=data['id'], student_id=sid).first()
            selection.pass_status = NOT_PASSING
            selection.save()
        return APIResult({
            "result": True,
            "message": "修改成功"
        })
    return APIServerError(data['message'])


def export_excel(request):
    token = request.GET['token']
    data = check_token(token)
    if data['res']:
        selections = Selection.objects.filter(teacher_id=data['id'], pass_status=PENDING)
        if selections:
            excel = Workbook(encoding='utf-8')
            sheet = excel.add_sheet('本科学生列表')
            header = ['学号', '姓名', '性别', '年级', '学院', '专业', '班级', '绩点', '绩点排名', '手机号码', '邮箱', '个人简介', '获奖情况', '志愿']
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
                    student.phone,
                    student.email,
                    student.profile,
                    student.award,
                    "第一志愿" if selection.is_first else "第二志愿"
                ]
                for index, value in enumerate(excel_data):
                    sheet.write(row, index, value)
                row += 1
            output = BytesIO()
            excel.save(output)
            output.seek(0)
            response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename={0}'.format(
                urlquote("学生选择信息表{0}.xls".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))
            return response
        else:
            return APIServerError('error')
    return HttpResponse("无数据")


def get_all_students(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            admin = Administrator.objects.get(username=data['id'])
            select_round = OpeningTime.objects.filter(grade=admin.grade).order_by('-s_end_time').first().round
            res = []
            students = Student.objects.filter(grade=Administrator.objects.get(username=data['id']).grade)
            for student in students:
                temp = {
                    "id": student.id,
                    "name": student.name,
                    "avatar": "http://localhost:8001" + student.avatar.url,
                    "class_name": student.class_name,
                    "gpa": student.gpa,
                    "first_aspiration": "",
                    "first_res": "",
                    "second_aspiration": "",
                    "second_res": "",
                    "subject": student.subject,
                    "profile": student.profile,
                    "award": student.award,
                    "phone": student.phone,
                    "email": student.email,
                    "agree_distribution": "是" if student.agree_distribution else "否"
                }
                selections = Selection.objects.filter(student_id=student.id, round=student.get_round())
                for selection in selections:
                    if selection.is_first:
                        temp['first_aspiration'] = selection.teacher.name
                        temp['first_res'] = PASS_STATUS[selection.pass_status]
                    else:
                        temp['second_aspiration'] = selection.teacher.name
                        temp['second_res'] = PASS_STATUS[selection.pass_status]
                res.append(temp)
            return APIResult({
                "students": res,
                "round": select_round
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


def get_all_teachers(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            teachers_res = []
            teachers = Teacher.objects.all()
            for teacher in teachers:
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
                "options": Teacher.get_institute_list()
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


def get_all_teachers_by_institute(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    institutes = request_post['institutes']
    data = check_token(token)
    if data['res']:
        teachers = Teacher.objects.filter(institute__in=institutes)
        teachers_res = []
        for teacher in teachers:
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
    return APIServerError(data['message'])


def get_round_selection(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            admin = Administrator.objects.get(username=data['id'])
            opening_time = OpeningTime.objects.filter(grade=admin.grade).order_by('-s_end_time')
            if opening_time:
                opening_time = opening_time.first()
                if opening_time.round == 1:
                    return APIResult({
                        'options': [{
                            'label': '第一轮选择',
                            'value': '1',
                            'disabled': True
                        }, {
                            'label': '第二轮选择',
                            'value': '2'
                        }]
                    })
            return APIResult({
                'options': [{
                    'label': '第一轮选择',
                    'value': '1'
                }, {
                    'label': '第二轮选择',
                    'value': '2',
                    'disabled': True
                }]
            })
        return APIServerError('error')
    return APIServerError(data['message'])


def open_selection(request):
    request_post = json.loads(request.body)
    from_format = "%Y-%m-%dT%H:%M:%S.000Z"
    token = request_post['token']
    select_round = eval(request_post['round'])
    student_date = request_post['studentDate']
    s_start = trans_format(student_date[0], from_format)
    s_end = trans_format(student_date[1], from_format)
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            admin = Administrator.objects.get(username=data['id'])
            selections = Selection.objects.filter(pass_status=PENDING)
            for selection in selections:
                if selection.student.grade == admin.grade:
                    return APIServerError("还有老师未进行确认，请先提醒后再开启下一轮选择！")
            opening_time = OpeningTime.objects.filter(grade=admin.grade).order_by('-s_end_time')
            if opening_time:
                opening_time = opening_time.first()
                if ((opening_time.round == 1 and select_round == 2) or (
                                opening_time.round == 2 and select_round == 1)) and opening_time.s_end_time.replace(
                    tzinfo=None) > s_start:
                    return APIServerError("上一轮选择还没结束！")
            OpeningTime.objects.create(grade=admin.grade, admin=admin, round=select_round,
                                       s_start_time=s_start, s_end_time=s_end)
            return APIResult({
                "result": True
            })
        return APIServerError('error')
    return APIServerError(data['message'])


def get_no_action_teachers(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            res = []
            teachers = Teacher.objects.all()
            grade = Administrator.objects.get(username=data['id']).grade
            for teacher in teachers:
                selections = Selection.objects.filter(teacher=teacher)
                if selections:
                    for selection in selections:
                        if selection.student.grade == grade and selection.pass_status == PENDING:
                            res.append({
                                "id": teacher.id,
                                "name": teacher.name,
                                "college": teacher.college,
                                "institute": teacher.institute,
                                "subject": teacher.subject,
                                "profile": teacher.profile
                            })
                            break
            return APIResult({
                "teachers": res
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


def get_no_action_students(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            res = []
            grade = Administrator.objects.get(username=data['id']).grade
            students = Student.objects.filter(grade=grade)
            for student in students:
                selections = Selection.objects.filter(student_id=student.id)
                if not selections:
                    temp = {
                        "id": student.id,
                        "name": student.name,
                        "avatar": "http://localhost:8001" + student.avatar.url,
                        "class_name": student.class_name,
                        "gpa": student.gpa,
                        "first_aspiration": "",
                        "first_res": "",
                        "second_aspiration": "",
                        "second_res": "",
                        "subject": student.subject,
                        "profile": student.profile,
                        "award": student.award,
                        "phone": student.phone,
                        "email": student.email,
                        "agree_distribution": "是" if student.agree_distribution else "否"
                    }
                    res.append(temp)
            return APIResult({
                "students": res
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


def automatically_assign_teacher(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            res = []
            grade = Administrator.objects.get(username=data['id']).grade
            students = Student.objects.filter(grade=grade)
            teachers = Teacher.objects.all()
            teachers = sorted(teachers, key=lambda x: x.get_student_count())
            index = 0
            count = 1
            for student in students:
                if not Selection.objects.filter(student=student, pass_status=PASSING):
                    if teachers[index].get_student_count() + count >= MAX_NUM:
                        index += 1
                        count = 1
                    res.append({
                        "id": student.id,
                        "name": student.name,
                        "avatar": "http://localhost:8001" + student.avatar.url,
                        "class_name": student.class_name,
                        "gpa": student.gpa,
                        "subject": student.subject,
                        "profile": student.profile,
                        "award": student.award,
                        "phone": student.phone,
                        "email": student.email,
                        "agree_distribution": "是" if student.agree_distribution else "否",
                        "assigned_teacher": teachers[index].name,
                        "t_id": teachers[index].id
                    })
            return APIResult({
                "students": res
            })
        return APIServerError('error')
    return APIServerError(data['message'])


def submit_distribution(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    form = request_post['tableData']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            for info in form:
                Selection.objects.get_or_create(teacher=Teacher.objects.get(id=info['t_id']),
                                                student=Student.objects.get(id=info['id']),
                                                round=-1)
            return APIResult({
                "result": True
            })
        return APIServerError('error')
    return APIServerError(data['message'])


def get_teacher_confirm_res(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            res = []
            is_finished = True
            grade = Administrator.objects.get(username=data['id']).grade
            students = Student.objects.filter(grade=grade)
            for student in students:
                selections = Selection.objects.filter(student_id=student.id, round=-1)
                if selections:
                    selection = selections.first()
                    if selection.pass_status == PENDING:
                        is_finished = False
                    temp = {
                        "id": student.id,
                        "name": student.name,
                        "avatar": "http://localhost:8001" + student.avatar.url,
                        "class_name": student.class_name,
                        "gpa": student.gpa,
                        "first_aspiration": selection.teacher.name,
                        "first_res": PASS_STATUS[selection.pass_status],
                        "second_aspiration": "",
                        "second_res": "",
                        "subject": student.subject,
                        "profile": student.profile,
                        "award": student.award,
                        "phone": student.phone,
                        "email": student.email,
                        "agree_distribution": "是" if student.agree_distribution else "否"
                    }
                    res.append(temp)
            return APIResult({
                "students": res,
                "isFinished": is_finished
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


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


def trans_format(time_string, from_format):
    """
    @note 时间格式转化
    :param time_string:
    :param from_format:
    :param to_format:
    :return:
    """
    time_struct = time.strptime(time_string, from_format)
    timestamp = time.mktime(time_struct) + 8 * 60 * 60
    times = datetime.datetime.fromtimestamp(timestamp)
    return times


def is_in_time(data):
    user_type = data['type']
    if user_type == 'student':
        student = Student.objects.get(id=data['id'])
        opening_time = OpeningTime.objects.filter(grade=student.grade).order_by('-s_end_time').first()
        if datetime.datetime.now() > opening_time.s_end_time.replace(tzinfo=None):
            return False, "本轮选择已经结束！如有问题请联系管理员。"
        elif datetime.datetime.now() < opening_time.s_start_time.replace(tzinfo=None):
            return False, "本轮选择还没开始！请耐心等待。"
        return True, ""
