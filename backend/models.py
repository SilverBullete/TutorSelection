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
    profile = models.TextField(default="", verbose_name="个人简介")
    award = models.TextField(default="", verbose_name="获奖情况")
    agree_distribution = models.BooleanField(default=False, verbose_name="接受分配")
    objects = models.Manager()


class Teacher(models.Model):
    id = models.CharField(max_length=12, primary_key=True, verbose_name="工号")
    password = models.CharField(max_length=50, default="", verbose_name="密码")
    name = models.CharField(max_length=50, default="", verbose_name="教师姓名")
    gender = models.IntegerField(choices=GENDER_CHOICE, default=0, verbose_name="性别")
    avatar = models.ImageField(upload_to=get_path, verbose_name="教师头像")
    college = models.CharField(max_length=50, default="", verbose_name="学院名称")
    institute = models.CharField(max_length=50, default="", verbose_name="导师研究机构")
    subject = models.CharField(max_length=50, default="", verbose_name="导师方向")
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
    pass_status = models.IntegerField(choices=PASS_CHOICE, default=0, verbose_name="通过情况")
    objects = models.Manager()


class Publicity(models.Model):
    id = models.AutoField
    grade = models.CharField(max_length=4, default="", verbose_name="年级")
    content = models.TextField(verbose_name="公示内容")
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, verbose_name="发布者")
    start_time = models.DateTimeField(default=datetime.now, verbose_name="开始公示时间")
    end_time = models.DateTimeField(default=datetime.now, verbose_name="公示结束时间")
    objects = models.Manager()


class OpeningTime(models.Model):
    id = models.AutoField
    grade = models.CharField(max_length=4, default="", verbose_name="年级")
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE, verbose_name="开放者")
    start_time = models.DateTimeField(default=datetime.now, verbose_name="开始开放时间")
    end_time = models.DateTimeField(default=datetime.now, verbose_name="公示开放时间")
    objects = models.Manager()


class File(models.Model):
    id = models.AutoField
    file = models.FileField(upload_to="file")
    publicity = models.ForeignKey(Publicity, on_delete=models.CASCADE, verbose_name="公示")
    objects = models.Manager()
