import os

from datetime import datetime
from django.db import models

GENDER_CHOICE = (
    (0, '男'),
    (1, '女')
)

PASS_CHOICE = (
    (0, '通过'),
    (1, '待通过'),
    (2, '未通过')
)

TYPE_CHOICE = (
    (0, '开放公告'),
    (1, '公示公告'),
    (2, '普通公告')
)


def get_path(instance, filename):
    filename = filename.split("\\")[-1]
    ext = filename.split('.').pop()
    filename = '{0}.{1}'.format(instance.id, ext)
    return os.path.join('image/', filename)


class Student(models.Model):
    id = models.CharField(max_length=12, primary_key=True, verbose_name="学号")
    password = models.CharField(max_length=50, default="", verbose_name="密码")
    name = models.CharField(max_length=50, default="", verbose_name="学生姓名")
    gender = models.IntegerField(choices=GENDER_CHOICE, default=0, verbose_name="性别")
    avatar = models.ImageField(upload_to=get_path, verbose_name="学生头像")
    grade = models.CharField(max_length=4, default="", verbose_name="年级")
    college = models.CharField(max_length=50, default="", verbose_name="学院名称")
    subject = models.CharField(max_length=50, default="", verbose_name="专业名称")
    class_name = models.CharField(max_length=50, default="", verbose_name="班级名称")
    gpa = models.FloatField(default=0, verbose_name="绩点")
    rank = models.CharField(max_length=50, default="", verbose_name="绩点排名")
    phone = models.CharField(max_length=11, default="", verbose_name="手机号")
    email = models.CharField(max_length=50, default="", verbose_name="邮箱")
    profile = models.TextField(default="", verbose_name="个人简介")
    award = models.TextField(default="", verbose_name="获奖情况")
    agree_distribution = models.BooleanField(default=False, verbose_name="接受分配")
    objects = models.Manager()

    def get_round(self):
        select_round = OpeningTime.objects.filter(grade=self.grade).order_by('-s_end_time').first().round
        selections = Selection.objects.filter(student=self)
        if select_round == 1:
            return select_round
        if selections.filter(round=1, pass_status=0):
            return 1
        if selections.filter(round=2, pass_status=0):
            return 2
        else:
            return -1

    def get_tutor(self):
        selections = Selection.objects.filter(round=self.get_round(), student=self, pass_status=0).order_by('-is_first')
        if selections:
            return selections.first().teacher.name
        return "暂无"


class Teacher(models.Model):
    id = models.CharField(max_length=12, primary_key=True, verbose_name="工号")
    password = models.CharField(max_length=50, default="", verbose_name="密码")
    name = models.CharField(max_length=50, default="", verbose_name="教师姓名")
    gender = models.IntegerField(choices=GENDER_CHOICE, default=0, verbose_name="性别")
    avatar = models.ImageField(upload_to=get_path, verbose_name="教师头像")
    college = models.CharField(max_length=50, default="", verbose_name="学院名称")
    institute = models.CharField(max_length=50, default="", verbose_name="导师研究机构")
    subject = models.CharField(max_length=50, default="", verbose_name="导师方向")
    phone = models.CharField(max_length=11, default="", verbose_name="手机号")
    email = models.CharField(max_length=50, default="", verbose_name="邮箱")
    profile = models.TextField(default="", verbose_name="个人简介")
    award = models.TextField(default="", verbose_name="获奖情况")
    objects = models.Manager()

    @staticmethod
    def get_institute_list():
        institutes = Teacher.objects.values("college", "institute")
        data = []
        for institute in institutes:
            if institute not in data:
                data.append(institute)
        institutes = sorted(data, key=lambda k: k['college'])
        res = []
        college = ""
        for institute in institutes:
            if institute['college'] != college:
                college = institute['college']
                res.append({
                    'value': college,
                    'label': college,
                    'children': [{
                        'value': institute['institute'],
                        'label': institute['institute']
                    }]
                })
            else:
                res[-1]['children'].append({
                    'value': institute['institute'],
                    'label': institute['institute']
                })
        return res

    def get_student_count(self):
        count = 0
        selections = Selection.objects.filter(teacher=self, pass_status=0)
        for selection in selections:
            if selection.is_first:
                count += 1
            else:
                if Selection.objects.filter(student=selection.student, is_first=True, pass_status=0):
                    continue
                count += 1
        return count


class Administrator(models.Model):
    id = models.AutoField
    username = models.CharField(max_length=12, default="", verbose_name="登录账号")
    password = models.CharField(max_length=50, default="", verbose_name="密码")
    grade = models.CharField(max_length=50, default="", verbose_name="管理年级")
    objects = models.Manager()


class Selection(models.Model):
    id = models.AutoField
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="导师")
    is_first = models.BooleanField(default=True, verbose_name="是否为第一志愿导师")
    pass_status = models.IntegerField(choices=PASS_CHOICE, default=1, verbose_name="通过情况")
    round = models.IntegerField(default=0, verbose_name="第几轮结果")
    objects = models.Manager()


class Publicity(models.Model):
    id = models.AutoField
    grade = models.CharField(max_length=4, default="", verbose_name="年级")
    title = models.CharField(max_length=50, default="", verbose_name="标题")
    content = models.TextField(verbose_name="公示内容")
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, verbose_name="发布者")
    start_time = models.DateTimeField(default=datetime.now, verbose_name="开始时间")
    end_time = models.DateTimeField(default=datetime.now, verbose_name="结束时间")
    publicity_type = models.IntegerField(choices=TYPE_CHOICE, default=2, verbose_name="公示类别")
    objects = models.Manager()


class OpeningTime(models.Model):
    id = models.AutoField
    grade = models.CharField(max_length=4, default="", verbose_name="年级")
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, verbose_name="开放者")
    round = models.IntegerField(default=0, verbose_name="第几轮")
    s_start_time = models.DateTimeField(default=datetime.now, verbose_name="学生选择开始时间")
    s_end_time = models.DateTimeField(default=datetime.now, verbose_name="学生选择结束时间")
    objects = models.Manager()


class Institute(models.Model):
    id = models.AutoField
    college = models.CharField(max_length=50, default="", verbose_name="学院名称")
    name = models.CharField(max_length=50, default="", verbose_name="导师研究机构")
    introduction = models.TextField(verbose_name="简介")
    objects = models.Manager()


class File(models.Model):
    id = models.AutoField
    file = models.FileField(upload_to="file")
    publicity = models.ForeignKey(Publicity, on_delete=models.CASCADE, verbose_name="公示")
    objects = models.Manager()
