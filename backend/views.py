import json
import datetime
import time

from io import BytesIO
from xlwt import *
from django.views.decorators.http import require_POST
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt

from .models import Student, Teacher, Administrator, Selection, Publicity, OpeningTime, Institute
from .response import APIResult, APIServerError
from .encryption import encrypt_password, certify_token, generate_token, validate_password
from TutorSelection.settings import MEDIA_ROOT

MAX_NUM = 8
PASSING = 0
PENDING = 1
NOT_PASSING = 2
PASS_STATUS = ['通过', '待通过', '未通过']


@csrf_exempt
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


@csrf_exempt
def get_user_type(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    data = check_token(token)
    if data['res']:
        return APIResult({
            "type": data['type']
        })
    return APIServerError(data['message'])


def init(request):
    Student.objects.create(id="201700000000", password=encrypt_password("123456"), name="学生1", grade="2018",
                           college="计算机学院", subject="软件工程", class_name="软工1803", gpa=4.5, rank="1/28",
                           phone="12345678910", email="201700000000@zjut.edu.cn")
    Student.objects.create(id="201700000001", password=encrypt_password("123456qaz"), name="学生2", grade="2018",
                           college="计算机学院", subject="软件工程", class_name="软工1803", gpa=4.4, rank="2/28",
                           phone="12345678910", email="201700000001@zjut.edu.cn")
    Student.objects.create(id="201700000002", password=encrypt_password("123456qaz"), name="学生3", grade="2018",
                           college="计算机学院", subject="软件工程", class_name="软工1803", gpa=4.3, rank="4/28",
                           phone="12345678910", email="201700000002@zjut.edu.cn")
    Student.objects.create(id="201700000003", password=encrypt_password("123456qaz"), name="学生4", grade="2018",
                           college="计算机学院", subject="软件工程", class_name="软工1803", gpa=4.2, rank="5/28",
                           phone="12345678910", email="201700000003@zjut.edu.cn")
    Student.objects.create(id="201700000004", password=encrypt_password("123456qaz"), name="学生5", grade="2018",
                           college="计算机学院", subject="软件工程", class_name="软工1803", gpa=4.1, rank="6/28",
                           phone="12345678910", email="201700000004@zjut.edu.cn")
    Student.objects.create(id="201700000005", password=encrypt_password("123456qaz"), name="学生6", grade="2018",
                           college="计算机学院", subject="软件工程", class_name="软工1803", gpa=4.0, rank="7/28",
                           phone="12345678910", email="201700000005@zjut.edu.cn")
    Student.objects.create(id="201700000006", password=encrypt_password("123456qaz"), name="学生7", grade="2018",
                           college="计算机学院", subject="软件工程", class_name="软工1803", gpa=2.5, rank="17/28",
                           phone="12345678910", email="201700000006@zjut.edu.cn")
    Teacher.objects.create(id="000000000000", password=encrypt_password("123456qaz"), name="丁维龙", college="计算机学院",
                           institute="计算机网络研究所", subject="虚拟仿真、人工智能与医学图像处理", phone="",
                           email="wlding@zjut.edu.cn", profile="http://www.cs.zjut.edu.cn/staffs/weilongding.html")
    Teacher.objects.create(id="000000000001", password=encrypt_password("123456qaz"), name="孙国道", college="计算机学院",
                           institute="计算机网络研究所", subject="大数据（时空数据、文本数据，视觉数据等）的挖掘、可视化、可视分析及其应用",
                           phone="", email="guodao@zjut.edu.cn",
                           profile="http://www.cs.zjut.edu.cn/staffs/guodaosun.html")
    Teacher.objects.create(id="000000000002", password=encrypt_password("123456qaz"), name="李燕君", gender=1,
                           college="计算机学院",
                           institute="计算机网络研究所", subject="智能物联网、室内定位、位置隐私保护", phone="",
                           email="yjli@zjut.edu.cn", profile="http://www.cs.zjut.edu.cn/staffs/yanjunli.html")
    Teacher.objects.create(id="000000000003", password=encrypt_password("123456qaz"), name="刘义鹏", college="计算机学院",
                           institute="计算机网络研究所", subject="模式识别", phone="", email="liuyipeng@zjut.edu.cn",
                           profile="http://www.cs.zjut.edu.cn/staffs/yipengliu.html")
    Teacher.objects.create(id="000000000004", password=encrypt_password("123456qaz"), name="范菁", gender=1,
                           college="计算机学院",
                           institute="计算机软件研究所", subject="服务计算、虚拟现实", phone="", email="fanjing@zjut.edu.cn",
                           profile="http://www.cs.zjut.edu.cn/staffs/jingfan.html")
    Teacher.objects.create(id="000000000005", password=encrypt_password("123456qaz"), name="沈国江", college="计算机学院",
                           institute="计算机智能系统研究所", subject="大数据分析、人工智能、智慧交通", phone="", email="gjshen1975@zjut.edu.cn",
                           profile="http://www.cs.zjut.edu.cn/staffs/guojiangshen.html")
    Teacher.objects.create(id="000000000006", password=encrypt_password("123456qaz"), name="陈胜勇", college="计算机学院",
                           institute="计算机视觉研究所", subject="计算机视觉、图像处理、机器人智能技术", phone="", email="csy@zjut.edu.cn",
                           profile="http://www.cs.zjut.edu.cn/staffs/shengyongchen.html")
    Teacher.objects.create(id="000000000007", password=encrypt_password("123456qaz"), name="王卫红", college="计算机学院",
                           institute="空间信息计算研究所", subject="遥感、网络安全", phone="", email="wwh@zjut.edu.cn",
                           profile="http://www.cs.zjut.edu.cn/staffs/weihongwang.html")
    Teacher.objects.create(id="000000000008", password=encrypt_password("123456qaz"), name="高飞", college="计算机学院",
                           institute="图形图像研究所", subject="视觉图像大数据分析、感知与理解", phone="", email="feig@zjut.edu.cn",
                           profile="http://www.cs.zjut.edu.cn/staffs/feigao.html")
    Administrator.objects.create(username="admin", password=encrypt_password("123456"), grade="2018")
    Institute.objects.create(college="计算机学院", name="计算机网络研究所",
                             introduction="计算机网络研究所在计算机网络、模式识别与智能系统、大数据等方面承担国家和社会重大需求任务，主持国家重点研发计划项目、国家自然基金重大仪器和重点基金项目等40余项，纵横向累积科研到款4700余万元。在智能感知、高效联网、智能系统、大数据处理等方面提出了一系列新的理论和方法，与行业龙头企业合作并在智慧交通、医疗、农业和工程等方面得到应用，取得了重大的社会经济效益。\n研究所共发表学术论文200余篇，其中Top期刊、CCF A类、中科院1区SCI论文50多篇，授权发明专利80多项，其中已转让10多项。相关成果获浙江省科技进步一等奖、教育部二等奖、浙江省自然科学奖二等奖、浙江省高校优秀科研成果一等奖在内的各类奖项10余项。\n计算机网络研究所是计算机学院最大的研究所，有专任教师33名，教授8名，副教授11名，具有博士学位老师比例为100%，在读全日制博士生30余名，在读全日制硕士生100多名。")
    Institute.objects.create(college="计算机学院", name="计算机软件研究所",
                             introduction=" 计算机软件研究所紧紧抓住学科发展的前沿问题，结合国家和浙江省软件产业发展的战略目标，开展计算机软件的理论、方法及其应用研究。研究所主要在软件服务理论与方法、虚拟现实方法与技术、信息安全技术与应用等方向上积累了丰硕成果，多项研究成果已达到国际先进水平。近年来研究所承担了国家重点研发计划课题1项、子课题2项、国家自然科学基金10多项、工信部工业互联网创新发展重大工程项目，以及多项浙江省自然科学基金、浙江省重点科技创新团队等项目。在工程应用和社会服务方面，成功开发了基于WEB SERVICES的信用构件库、身份公钥密钥管理服务系统、网络安全攻防演练平台、虚拟森林动态生长模拟系统、森林通道绿化模拟系统等软件，在多个社会工程系统中得到应用，助力浙江省软件工程、网络安全等产业高地建设持续发展，服务浙江省数字经济一号工程。\n研究所与众多国内外的知名大学和研究机构建立了密切的联系与友好的科研合作交流关系，包括美国的卡内基梅陇大学、华盛顿大学、辛辛那提大学、加拿大的圣弗朗西斯泽维尔大学、英国的阿伯丁大学、伦敦大学、埃塞克斯大学、澳大利亚的昆士兰大学，以及国内的清华大学、北京航空航天大学、浙江大学、香港科技大学等。\n研究所成员在IEEE TKDE、TMC、IEEE VR、ACM CHI、CSCW等CCF A类及其他知名期刊或国际会议发表论文100多篇，获得省部级科技奖2项，拥有发明专利、软件著作权100多项。")
    Institute.objects.create(college="计算机学院", name="计算机智能系统研究所",
                             introduction="计算机智能系统是目前计算机基础科学和应用学科中发展最快、应用最广的研究领域之一。本学科方向紧紧围绕数字经济“一号工程”的“卡脖子”关键核心技术和前沿基础理论研究，以重大行业应用需求为目标，以信息系统的智能处理为主线，依托研究所在理论、系统、网络等方面的优势，从信息的获取、表示、理解与转换等几个方面进行布局，构成了一个互为依托的有机整体。实现国家、社会、行业、民生等城市公共事业、重大工业行业、特殊行业等的智能化“自主可控”。在智能决策集成方面的理论、方法与技术问题展开深入研究，取得了多项具有国际先进水平的成果。\n研究所在计算机智能系统方面承担国家和社会重大需求任务，主持国家863项目、国家自然科学基金项目近40项，浙江省重大科技计划项目及其它省部项目近40项，在计算机智能系统领域提出了一系列新的理论和方法。在工程应用上，与行业龙头企业联合开发了电力、交通、未来社区、城市大脑、化工、印染、交通、水电、旅游、物流等多个重大智能系统，取得了重大的社会经济效益。\n在国际著名期刊上发表SCI论文200多篇，被国内外专家学者引用4000余次。在科学出版社、高等教育出版社等编著10多部中文著作。获得国家级教学成果奖1项，省部级教学成果奖1项，省部级科技奖10多项，取得授权发明专利70多项，专利技术转让10多项，为国内50多家企业进行创新支持和技术指导。\n研究所目前已形成一支具有创新精神、年龄结构合理的学科队伍，现有固定研究人员25名、研究生80多名，包括国家教学名师、国务院政府特贴专家、入选国家“万人计划”各1人，教授4人，副教授12人，80%具有博士学位和具有海外留学经历。")
    Institute.objects.create(college="计算机学院", name="计算机视觉研究所",
                             introduction="计算机视觉是目前人工智能和计算机学科中应用最广的研究领域之一。本研究所关注计算机视觉、多媒体信息处理、图像处理、医学影像计算、人工智能、模式识别等领域的前沿理论研究，致力于将计算机视觉和人工智能相关的理论技术转化为实际应用系统，实现智能制造、智慧安防、信息处理、生产过程监测的自动化和智能化，取得多项具有国际先进水平的成果。\n研究所在计算机视觉及相关应用方面承担国家和社会重大需求任务，主持国家杰出青年科学基金、国家重点研发计划、国家自然科学基金重点、面上、青年项目30余项，浙江省重大科技计划项目及其它省部项目40多项。在理论上提出了一系列适合于实际环境的新理论和新方法，并在多个工程系统中得到应用，获得省部级科技奖6项，取得授权发明专利80多项，部分技术立于国际前沿地位。在国际著名期刊发表SCI论文300多篇，其中影响因子5.0以上的论文20多篇。被国内外专家学者引用6000余次。在Springer、科学出版社等编著20多部英文学术著作、10部中文著作。5人次获IEEE等国际学术最佳论文奖，20篇论文入选ESI高被引论文。专利技术转让20余项，为国内50多家企业进行创新支持和技术指导。 \n研究所目前已形成一支具有创新精神、年龄结构合理的学科队伍，现有固定研究人员18名、研究生100多名，包括国家教学名师、国务院政府特贴专家、入选国家“万人计划”各1人，教授4人，副教授7人，都具有博士学位，80%具有海外留学经历。")
    Institute.objects.create(college="计算机学院", name="空间信息计算研究所",
                             introduction="空间信息计算研究所主要研究方向为遥感、GIS、云计算、隐私保护与数据挖掘等，研究所围绕空间信息科学，结合人工智能和云计算等最新的理论与及技术，在遥感图像信息提取、空间大数据分析、网络安全、GIS应用等领域展开深入研究，取得多项国内领先的技术成果。\n研究所在空间信息科学领域承担国家和社会重大需求任务，主持国家863项目、国家自然科学基金项目近十余项，浙江省重大科技计划项目及其它省部项目近多项，申请或者授权60多项。在工程应用上，研究所成果已在国土资源调查、农林业遥感数据智能提取等领域成功应用，为国内多家企业进行创新支持和技术指导。\n研究所目前已形成一支具有创新精神、年龄结构合理的学科队伍，现有固定研究人员10名、研究生40多名，包括教授3人，副教授2人，80%具有博士学位和具有海外留学经历。")
    Institute.objects.create(college="计算机学院", name="图形图像研究所",
                             introduction="研究所有12名专任教师，其中教授2人，副教授6人，教师队伍中有8人具有博士学位，大部分来自清华大学、浙江大学、上海交通大学等名校且具有海外留学背景。\n研究所主要从事视频图像大数据、智能制造、知识图谱等方面的研究与开发，主持或参与图家重点研发计划、国家自然科学基金、浙江省重点研发计划、浙江省自然科学基金及横向项目150余项。获省科技进步奖三等奖5项,浙江省高校科技进步三等奖2项、浙江省人事科研成果一等奖2项，浙江省科技成果三等奖1项，国家人事部人事科研成果二等奖1项，浙江工业大学教学成果奖1等奖，省高校优秀科研成果奖二等奖2项，获国家发明、实用新型专利和软件著作权近400余项，已在《机械工程学报》、《软件学报》、《计算机学报》、《计算机辅助设计与图形学学报》、《IEEE Trans. On Instru. and Meas.》、《Computer-Aided Design》、《The International Journal of Advanced Manufacturing Technology》、《Computers in Industry》等国内外重要期刊、国际学术会议发表论文400余篇，出版教材和专著4部，培养研究生近100人。\n研究所秉承“顶天立地”的理念，力求将理论研究和工程应用相结合，跟踪国际学术前沿，并紧密结合浙江经济社会发展和企业需求。展望未来，我们将努力把研究所建设成为前沿学术研究的基地、高新技术创新的源头和高级人才培养的摇篮。")
    Publicity.objects.create(grade="2018", title="test公告", content="['测试测试','测试']",
                             admin=Administrator.objects.get(username="admin"))
    OpeningTime.objects.create(grade="2018", admin=Administrator.objects.get(username="admin"), round=1,
                               s_end_time=datetime.datetime.fromtimestamp(1612622841))
    Selection.objects.create(student=Student.objects.get(id="201700000001"),
                             teacher=Teacher.objects.get(id="000000000000"), round=1)
    Selection.objects.create(student=Student.objects.get(id="201700000002"),
                             teacher=Teacher.objects.get(id="000000000000"), round=1, pass_status=0)
    Selection.objects.create(student=Student.objects.get(id="201700000003"),
                             teacher=Teacher.objects.get(id="000000000000"), round=1, pass_status=2)
    Selection.objects.create(student=Student.objects.get(id="201700000001"),
                             teacher=Teacher.objects.get(id="000000000001"), is_first=False, round=1, pass_status=0)
    Selection.objects.create(student=Student.objects.get(id="201700000002"),
                             teacher=Teacher.objects.get(id="000000000001"), is_first=False, round=1, pass_status=2)
    Selection.objects.create(student=Student.objects.get(id="201700000006"),
                             teacher=Teacher.objects.get(id="000000000000"), round=1)
    Selection.objects.create(student=Student.objects.get(id="201700000004"),
                             teacher=Teacher.objects.get(id="000000000000"), round=1)
    return APIResult({}, "添加成功")


@csrf_exempt
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
                "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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
                "avatar": "http://localhost:8001" + teacher.avatar.url if teacher.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
            })
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
                "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
def get_institute_info(request):
    request_post = json.loads(request.body)
    name = request_post['institute']
    institute = Institute.objects.filter(name=name)
    if institute:
        return APIResult({
            "info": institute.first().introduction
        })
    return APIServerError('error')


@csrf_exempt
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


@csrf_exempt
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
                    "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
                    "pass_status": selection.pass_status
                })
            return APIResult(res)
        else:
            return APIServerError('error')
    return APIServerError(data['message'])


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
                    "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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


@csrf_exempt
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
                "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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
                    "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
                    "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
                        "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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


@csrf_exempt
def automatically_assign_teacher(request):
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
                    return APIServerError("请先开放第二轮选择！")
                else:
                    if datetime.datetime.now < opening_time.s_end_time.replace(tzinfo=None):
                        return APIServerError("请先等待第二轮选择结束！")
            else:
                return APIServerError("请先开放第一轮选择！")
            res = []
            grade = Administrator.objects.get(username=data['id']).grade
            students = Student.objects.filter(grade=grade)
            teachers = Teacher.objects.all()
            teachers = sorted(teachers, key=lambda x: x.get_student_count())
            index = 0
            for student in students:
                if not Selection.objects.filter(student=student, pass_status=PASSING):
                    if teachers[index].get_student_count() + 1 >= MAX_NUM:
                        index = 0
                    res.append({
                        "id": student.id,
                        "name": student.name,
                        "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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
                    index += 1
            return APIResult({
                "students": res
            })
        return APIServerError('error')
    return APIServerError(data['message'])


@csrf_exempt
def submit_distribution(request):
    request_post = json.loads(request.body)
    token = request_post['token']
    form = request_post['tableData']
    data = check_token(token)
    if data['res']:
        if data['type'] == 'admin':
            admin = Administrator.objects.get(username=data['id'])
            opening_time = OpeningTime.objects.filter(grade=admin.grade).order_by('-s_end_time')
            if opening_time:
                opening_time = opening_time.first()
                if opening_time.round == 1:
                    return APIServerError("请先开放第二轮选择！")
                else:
                    if datetime.datetime.now < opening_time.s_end_time.replace(tzinfo=None):
                        return APIServerError("请先等待第二轮选择结束！")
            else:
                return APIServerError("请先开放第一轮选择！")
            for info in form:
                Selection.objects.get_or_create(teacher=Teacher.objects.get(id=info['t_id']),
                                                student=Student.objects.get(id=info['id']),
                                                round=-1)
            return APIResult({
                "result": True
            })
        return APIServerError('error')
    return APIServerError(data['message'])


@csrf_exempt
def get_teacher_confirm_res(request):
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
                    return APIServerError("请先开放第二轮选择！")
                else:
                    if datetime.datetime.now < opening_time.s_end_time.replace(tzinfo=None):
                        return APIServerError("请先等待第二轮选择结束！")
            else:
                return APIServerError("请先开放第一轮选择！")
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
                        "avatar": "http://localhost:8001" + student.avatar.url if student.avatar else "http://127.0.0.1:8001/media/bg/avatar.jpeg",
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
