#负责视图和路由
import hashlib


from flask import request
from flask import redirect
from flask import render_template,make_response
from flask import jsonify

from flask import session
from . import main
from app import csrf
from app.models import *
from .forms import *

#密码加密
def setpassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

@csrf.exempt
@main.route("/register/",methods=["GET","POST"])
def register():
    if request.method=='POST':
        form_data=request.form
        username=form_data.get("username")
        password=form_data.get("password")
        identity=form_data.get("identity")
        print(identity)
        print(type(identity))
        user=User()
        user.username=username
        user.password=setpassword(password)
        user.identity=int(identity)
        user.save()
        return redirect('/login/')
    students=Students.query.all()
    return render_template('register.html',**locals())
#注册验证ajax,get请求
#@app.route('/uservalid/')
# def uservalid():
#     result={
#         "code":"",
#         "data":""
#     }
#     data = request.args.get("username")
#     print(data)
#     if data:
#         user=User.query.filter_by(username=data).first()
#         if user:
#             result["code"]=400
#             result["data"]="用户已存在"
#         else:
#             result["code"] = 200
#             result["data"] = "用户名没有被注册，可使用"
#     return jsonify(result)
#注册名字校验ajax，post请求
@main.route('/uservalid/',methods=["GET","POST"])
def uservalid():
    result={
        "code":"",
        "data":""
    }
    if request.method=='POST':
        data = request.form.get("username")
        print(data)
        if data:
            user = User.query.filter_by(username=data).first()
            if user:
                result["code"] = 400
                result["data"] = "用户已存在"
            else:
                result["code"] = 200
                result["data"] = "用户名没有被注册，可使用"
        else:
            result["code"] = 400
            result["data"] = "请求方式错误"
    return jsonify(result)


@csrf.exempt
@main.route("/login/",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identity=form_data.get("identity")
        #print(identity)
        user = User.query.filter_by(username=username).first()
        send_password = setpassword(password)
        if user:
            db_password = user.password
            user_id=user.id
            user_identity=user.identity
            user_identity_id=user.identity_id


            #print(user_identity)
            if send_password == db_password and user_identity==int(identity):
                response = redirect('/index/')
                response.set_cookie("username",username)
                response.set_cookie("user_id",str(user_id))
                #设置cookie用来判断是学生还是老师，登录
                response.set_cookie("user_identity", str(user_identity))

                #判端是否完成了个人信息
                if user_identity == 0:
                    student = Students.query.filter_by(id=user.identity_id).first()
                    if user_identity_id and student:
                        student_name = student.name
                        response.set_cookie(" user_identity_id", str(user_identity_id))
                        response.set_cookie(" student_name", student_name)
                    else:
                        response.set_cookie(" user_identity_id", "")
                        response.set_cookie(" student_name", "")
                else:
                    teacher = Teacher.query.filter_by(id=user.identity_id).first()
                    if user_identity_id and teacher:
                        teacher_name = teacher.name
                        response.set_cookie(" user_identity_id", str(user_identity_id))
                        response.set_cookie(" teacher_name", teacher_name)
                    else:
                        response.set_cookie(" user_identity_id","")
                        response.set_cookie(" teacher_name","")

                session["username"]=user.username
                return response
    return render_template('login.html', **locals())
#用ajax校验，登录身份,get请求
@main.route('/identityvalid/',methods=["GET","POST"])
def identityvalid():
    result={"code":"","data":""}
    username=request.args.get("username")
    identity=request.args.get("identity")
    if username:
        user=User.query.filter_by(username=username).first()
        if user:
            result["code"] = 200
            result["data"] = "用户名正确"
            user_identity=user.identity
            if user_identity==int(identity):
                result["code"]=200
                result["data"]="用户身份验证正确可以登陆"
            else:
                result["code"] = 400
                result["data"] = "用户身份验证不正确，请重新登陆"
        else:
            result["code"] = 400
            result["data"] = "用户名不存在，请注册"
    else:
        result["code"] = 400
        result["data"] = "用户名不能为空"
    return jsonify(result)

#设置装饰器，来确定登录唯一性
import functools#flask装饰器解决问题
def loginvalid(fun):
    @functools.wraps(fun)
    def inner(*args,**kwargs):
        username=request.cookies.get("username")
        user_id=request.cookies.get("user_id")
        session_username=session.get("username")
        if username and user_id and session_username:
            if username==session_username:
                return fun(*args,**kwargs)
        return redirect('/login/')
    return inner

# @app.route("/student_list/",methods=["GET","POST"])
# def student_list():
#     students=Students.query.all()
#     return render_template('student_list.html',**locals())


@csrf.exempt

@main.route("/index/",methods=["GET","POST"])
@loginvalid
def index():
    #students=Students.query.all()
    user_identity=request.cookies.get("user_identity")

    if user_identity == "1":
            return redirect('/add_teacher/')
    else:
            return redirect('/add_student/')


@main.route("/student_list/",methods=["GET","POST"])
@loginvalid
def student_list():
    students=Students.query.all()

    return render_template('student_list.html',**locals())


#添加学生
@csrf.exempt#单视图函数避免csrf校验
@main.route("/add_student/",methods=["GET","POST"])
@loginvalid
def add_student():
    result={"data":""}
    user_id = request.cookies.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    user_identity_id=request.cookies.get("user_identity_id")
    #student = Students.query.filter_by(id=user.identity_id).first()
    # username=request.cookies.get("username")
    students_form = StudentsForm()
    if request.method=='POST':
        name=request.form.get("name")
        age=request.form.get("age")
        gender=request.form.get("gender")
        has_id=request.form.get("has_id")
        print(has_id)
        student1=Students.query.filter_by(name=name).first()
        # print(student)
        # print(student.has_id)
        if student1 and int(has_id)==1:
                user1=User.query.filter_by(identity_id=student1.id).first()
                if user1.username!=user.username:
                    result["data"]="此学生已被完善，请输入正确的信息"
                else:
                    user_identity_id = student1.id
                    user.save()
        else:
                s=Students()
                s.name=name
                s.age=age
                s.gender=gender
                s.has_id=1
                s.save()
                user.identity_id=s.id
                user.save()
                user_identity_id=user.identity_id
                student_name=s.name
                #student = Students.query.filter_by(id=user.identity_id).first()

                response = make_response(redirect('/add_student/'))
                #response=redirect('/add_student/')
                response.set_cookie("user_identity_id",str(user_identity_id))
                response.set_cookie(" student_name", student_name)

                return response
    return render_template('index.html',**locals())
@csrf.exempt#单视图函数避免csrf校验
@main.route('/student/',methods=["GET","POST"])
def student():
    # user_id = request.cookies.get("user_id")
    # user = User.query.filter_by(id=user_id).first()
    id=request.args.get("id")
    student=Students.query.filter_by(id=id).first()
    if request.method=='POST':
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        id=request.form.get("id")
        student = Students.query.filter_by(id=id).first()
        student.name=name
        student.age=age
        student.gender=gender
        student.save()
        student_name=student.name
        response=make_response(redirect('/student/?id=%s'%(student.id)))#重定向传参数，用get请求传参数
        response.set_cookie(" student_name", student_name)
        return response

    return render_template('student.html',**locals())
#选择课程
@csrf.exempt#单视图函数避免csrf校验
@main.route("/choice_course/",methods=["GET","POST"])
def choice_course():
    result={"content":""}
    id = request.args.get("id")
    student = Students.query.filter_by(id=id).first()
    user_id = request.cookies.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    course_list=Course.query.all()
    #print(course_list)
    if request.method=='POST':
        post_data=request.form
        course_listone=[]
        new_list=[]
        for k,v in post_data.items():
            if k.startswith("course_"):
                course_listone.append(int(v))
        #print(course_listone)
        models.session.add(student)
        course_lst=student.to_course.all()#多对多的查询
        #print(course_lst)
        if len(course_listone):
            for course_id in course_listone:
                course=Course.query.filter_by(id=course_id).first()
                if course not in course_lst:
                    new_list.append(course)
                    course.to_students.append(student)
            models.session.commit()
            return redirect('/course_list/')
        else:
            result["content"]="不能选择为空"

    return render_template('choice_course.html',**locals())
@main.route("/course_ajax/",methods=["GET","POST"])
def course_ajax():
    result = {"status":"success","content": ""}
    user_identity_id = request.cookies.get("user_identity_id")
    student=Students.query.get(user_identity_id)
    course_lt = student.to_course.all()#多对多关系查询，通过学生找到该学生的课程列表
    id = request.args.get("id")
    #print(id)
    course = Course.query.get(id)
    #print(course.lable)
    if course in course_lt:
        result["status"] = "error"
        result["content"] = "这课程你已选择，请不要重复选择"

    else:
        result["content"] = "这课程你没选择，可以选择"
    return jsonify(result)


# def course():
#     id=request.args.get("id")
#     course=Course.query.get(id)
#
#     return render_template('course.html',**locals())

#课程详情
@csrf.exempt#单视图函数避免csrf校验
@main.route("/course/",methods=["GET","POST"])
def course():
    id=request.args.get("id")
    course=Course.query.get(id)
    return render_template('course.html',**locals())

#课程列表
@csrf.exempt#单视图函数避免csrf校验
@main.route("/course_list/",methods=["GET","POST"])
def course_list():
    user_id = request.cookies.get("user_id")
    user = User.query.filter_by(id=user_id,identity=0).first()
    student=Students.query.filter_by(id=user.identity_id).first()
    course_list=student.to_course.all()
    lst=[]
    for course in course_list:
        teacher=course.to_teacher.all()

        result={
                "course":course,
                "teacher_list":teacher
            }

        lst.append(result)

    return render_template('course_list.html',**locals())


@csrf.exempt#单视图函数避免csrf校验
@main.route("/teacher_student/",methods=["GET","POST"])
def teacher_student():
    user_id = request.cookies.get("user_id")
    #user = User.query.filter_by(id=user_id, identity=0).first()
    user_identity_id = request.cookies.get("user_identity_id")
    student = Students.query.get(user_identity_id)
    #student = Students.query.filter_by(id=user.identity_id).first()
    if request.method=='POST':
        id=request.form.get("course_id")#获取课程id
        print(id)
        teacher_id=request.form.get("teacher_id")
        print(teacher_id)
        course=Course.query.filter_by(id=id).first()
        teacher=Teacher.query.get(int(teacher_id))
        print(teacher)

        models.session.add(student)
        teacher.to_students.append(student)
        models.session.commit()
    return redirect('/teacher_student_list/')

# ajax校验如果以选择老师，就不能在选了
@csrf.exempt#单视图函数避免csrf校验
@main.route("/teacher_ajax/", methods=["GET", "POST"])
def teacher_ajax():
        result = {"status": "success", "content": ""}
        user_identity_id = request.cookies.get("user_identity_id")
        student = Students.query.get(user_identity_id)  # 找到这个学生
        teacher_stu = student.to_teacher.all()  # 通过该学生找到所有的老师
        #print(teacher_stu)
        id = request.args.get("id")
        #print(id)
        course = Course.query.filter_by(id=id).first()
        teacher_lst = course.to_teacher.all()  # 通过这个课程知道了老师
        #print(teacher_lst)
        has_teacher = 0  # 设置这门专业有老师了，为1
        for teacher in teacher_lst:
            if teacher in teacher_stu:
                has_teacher = 1  # 这个专业老师在这个学生的老师类表中，证明这个专业老师已存在
        if has_teacher == 1:
            result["status"] = "error"
            result["content"] = "这门课程，你已选过老师，无需在选"

        else:
            result["content"] = "这门课程，你还没选老师，请选择"
        return jsonify(result)

#课程列表，专业，授课老师
@main.route("/teacher_student_list/",methods=["GET","POST"])
def teacher_student_list():
    user_id = request.cookies.get("user_id")
    user = User.query.filter_by(id=user_id, identity=0).first()
    student = Students.query.filter_by(id=user.identity_id).first()
    course_list=student.to_course.all()#通过学生找到他所选择的专业
    teacher_course_list=[]
    for course in course_list:
        teacher=student.to_teacher.filter_by(course_id=course.id).first()
        """
            通过学生找到所有的老师，然后在通过专业找到该专业老师
        """
        result={
            "course":course,
            "teacher":teacher
        }
        teacher_course_list.append(result)

    return render_template('teacher_student_list.html',**locals())

#学生考勤情况,本周考勤
@main.route("/student_attendance/",methods=["GET","POST"])
def student_attendance():
    user_id = request.cookies.get("user_id")
    user = User.query.filter_by(id=user_id, identity=0).first()
    student = Students.query.filter_by(id=user.identity_id).first()
    return render_template('student_attendance.html',**locals())
#在线申请请假
import time
#设置一函数把字符串转换成datetime格式
def date_time(test):
    timeArray = time.strptime(test, "%Y-%m-%d")  # 将字符串转换成time类型
    ask_datetime = datetime.datetime(*timeArray[:6])  # 将time类型转换成datetime类型
    return ask_datetime
@csrf.exempt#单视图函数避免csrf校验
@main.route("/student_online/",methods=["GET","POST"])
def student_online():
    result={"content":""}
    user_id = request.cookies.get("user_id")
    user = User.query.filter_by(id=user_id, identity=0).first()
    student = Students.query.filter_by(id=user.identity_id).first()
    course_list=student.to_course.all()
    if request.method=='POST':
        student_name=request.form.get("student_name")
        reason=request.form.get("reason")
        asktime=request.form.get("asktime")#获取form表单提交的字符串时间
        course_name=request.form.get("course_name")
        teacher_name=request.form.get("teacher_name")
        if student_name or reason or asktime or course_name or teacher_name:#输入的不能有一个为空
            print("jhahhah")
            if student.name==student_name:
                has_course=0#证明学生有此门课程
                for course in course_list:
                    if course_name==course.lable:
                        has_course=1
                if has_course==1:
                    course = Course.query.filter_by(lable=course_name).first()
                    course_id=course.id
                    teacher = student.to_teacher.filter_by(course_id=course_id).first()


                    if teacher_name==teacher.name:
                        teacher_id=teacher.id

                        ask=Ask()
                        ask.student_name=student_name
                        ask.reason=reason
                        ask_datetime = date_time(asktime)#转换时间格式
                        ask.asktime =  ask_datetime
                        nowtime = datetime.datetime.now()
                        ask.subtime = nowtime
                        ask.course_name=course_name
                        ask.teacher_name=teacher_name
                        ask.teacher_id=teacher_id
                        ask.student_id=student.id
                        print("hello")
                        ask.save()
                        return redirect('/ask_list/')
            else:
                result["content"]="同学你好，请输入你的名字，不能代替"
    return render_template('student_online.html',**locals())
#用ajax校验请假人是本人,用的是get请求
@csrf.exempt#单视图函数避免csrf校验
@main.route("/askname_ajax/", methods=["GET", "POST"])
def askname_ajax():
    result = {"status": "error", "content": ""}
    user_identity_id = request.cookies.get("user_identity_id")
    student = Students.query.get(user_identity_id)  # 找到这个学生
    student_name=request.args.get("student_name")
    print(student_name)
    if student_name:
        if student_name==student.name:
                result["status"]="success"
                result["content"]="确认是本人"
        else:
                result["content"] = "确认不是本人，重新输入"
    else:
            result["content"]="姓名不能为空"
    return jsonify(result)
#用ajax校验请假时间在当前时间之后,用的是get请求
@csrf.exempt#单视图函数避免csrf校验
@main.route("/asktime_ajax/", methods=["GET", "POST"])
def asktime_ajax():
    result = {"status": "error", "content": ""}
    asktime=request.args.get("asktime")#获取到的时间字符串
    if asktime:
        ask_date = date_time(str(asktime))  # 转换为date格式
        online_seconds = ask_date.timestamp()  # 把date格式的时间转换成时间戳
        print(online_seconds)
        nowtime = datetime.datetime.now()  # 获取当前时间,直接转换date格式
        online_seconds_now = nowtime.timestamp()  # 把date格式的时间转换成时间戳
        print(online_seconds_now)
        if online_seconds_now <= online_seconds:
            result["status"] = "success"
            result["content"] = "时间正确"
        else:
            result["content"] = "时间不对，请重新输入"

    else:
        result["content"] = "请假时间不能为空"
    return jsonify(result)
#用ajax校验请假的专业是必须是本学生选择的专业,用的是get请求
@csrf.exempt#单视图函数避免csrf校验
@main.route("/askcourse_ajax/", methods=["GET", "POST"])
def askcourse_ajax():
    result = {"status": "error", "content": ""}
    askcourse = request.args.get("course_name")  # 获取到的专业名字
    user_identity_id = request.cookies.get("user_identity_id")
    student = Students.query.get(user_identity_id)  # 找到这个学生
    course_list = student.to_course.all()#通过该学生找到此学生学的专业
    if askcourse:
        has_course=0
        #通过循环来判断输入的专业是此学生选择的
        for course in course_list:
            if  askcourse == course.lable:
                has_course=1
        if has_course==1:#有此专业
            result["status"] = "success"
            result["content"] = "有此学科"
        else:
            result["content"] = "你没有选择此学科，请重新输入"
    else:
        result["content"] = "专业不能为空"
    return jsonify(result)
#校验已选择此学科所对应的；老师是对的
@csrf.exempt#单视图函数避免csrf校验
@main.route("/askteacher_ajax/", methods=["GET", "POST"])
def askteacher_ajax():
    result = {"status": "error", "content": ""}
    askcourse = request.args.get("course_name")  # 获取到的专业名字
    user_identity_id = request.cookies.get("user_identity_id")
    student = Students.query.get(user_identity_id)  # 找到这个学生
    student_name = request.args.get("student_name")#获取到学生名字
    teacher_name = request.args.get("teacher_name")
    if student_name or askcourse:
        if teacher_name:
            course_id = Course.query.filter_by(lable=askcourse).first().id#通过填写的专业名字，找到id
            teacher = student.to_teacher.filter_by(course_id=course_id).first()#通过学生及专业id找到此专业的具体教师
            if teacher_name == teacher.name:
                result["status"] = "success"
                result["content"] = "有此教师"
            else:
                result["content"] = "没有此教师,请重新输入"

        else:
            result["content"] = "教师名字不能为空"

    else:
        result["content"] = "没有请假人和专业，无法选择老师"
    return jsonify(result)
#展示我的假条
@main.route("/ask_list/",methods=["GET","POST"])
def ask_list():
    return render_template("ask_list.html",**locals())

@csrf.exempt#单视图函数避免csrf校验
#csrf.error_headler重新定义403错误页
@loginvalid
@main.route("/add_teacher/",methods=["GET","POST"])

def add_teacher():
    result = {"data": ""}
    user_id = request.cookies.get("user_id")
    user_identity_id = request.cookies.get("user_identity_id")
    user = User.query.filter_by(id=user_id).first()
    teacher = Teacher.query.filter_by(id=user.identity_id).first()
    teacher_form = TeacherForm()
    if request.method == 'POST':
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course = request.form.get("course")
        teacher1 = Teacher.query.filter_by(name=name).first()
        if teacher1 and  user_identity_id:
            user1 = User.query.filter_by(identity_id=teacher1.id).first()
            if user1.username != user.username:
                result["data"] = "此教师已被完善，请输入正确的信息"
            else:
                user.identity_id = teacher1.id
                user.save()
        else:
            t = Teacher()
            t.name = name
            t.age = age
            t.gender = gender
            t.course_id = int(course)
            t.save()
            user.identity_id = t.id
            user.save()
            teacher_name=t.name
            user_identity_id= user.identity_id
            response = redirect('/add_teacher/')
            response.set_cookie("user_identity_id", str(user_identity_id))
            response.set_cookie("teacher_name", teacher_name)
            return response
    return render_template('index.html',**locals())
#展示老师信息
@csrf.exempt#单视图函数避免csrf校验
@main.route("/teacher/",methods=["GET","POST"])
def teacher():
    id=request.args.get("id")
    teacher=Teacher.query.filter_by(id=id).first()#通过get请求获取的id找到该老师

    if request.method=='POST':
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        id=request.form.get("id")
        teacher = Teacher.query.filter_by(id=id).first()
        teacher.name=name
        teacher.age=age
        teacher.gender=gender
        teacher.save()
        teacher_name=teacher.name
        response=make_response(redirect('/teacher/?id=%s'%(teacher.id)))#重定向传参数，用get请求传参数
        response.set_cookie(" teacher_name", teacher_name)
        return response
    return render_template('teacher.html',**locals())
#学生列表
@csrf.exempt#单视图函数避免csrf校验
@main.route("/student_message/",methods=["GET","POST"])
def student_message():
    user_identity_id = request.cookies.get("user_identity_id")
    teacher = Teacher.query.filter_by(id=user_identity_id).first()#获取老师信息
    student_list=teacher.to_students.all()
    student_course_teacher_list=[]
    #通过循环找到每个学生，在找到该学生学的专业，及相关老师
    for student in student_list:
       course_list=student.to_course.all()#获取学会的课程列表
       stu_list=[]#设置存储这个学生的专业与相关老师列表
       for course in course_list:
            teacher_lst=student.to_teacher.filter_by(course_id=course.id).first()
            result={
                "course":course,
                "teacher_lst":teacher_lst
                    }
            stu_list.append(result)
       stu={
           "student":student,
           "stu_list":stu_list
       }
       student_course_teacher_list.append(stu)
    print(student_course_teacher_list)
    return render_template('student_message.html',**locals())
#学生的假条
@csrf.exempt#单视图函数避免csrf校验
@main.route("/student_ask/",methods=["GET","POST"])
def student_ask():
    user_identity_id = request.cookies.get("user_identity_id")
    teacher = Teacher.query.filter_by(id=user_identity_id).first()  # 获取老师信息
    student_list = teacher.to_students.all()
    nowtime=datetime.datetime.now()
    now=nowtime.strftime("%Y/%m/%d ")
    s_lst=[]
    for student in student_list:
        # lst=student.to_ask#一对多的查询
        # print(lst)
        ask_count=Ask.query.filter_by(teacher_id=teacher.id,student_id=student.id).count()#获取该学生写给此老师的假条
        ask1_count=Ask.query.filter_by(teacher_id=teacher.id,student_id=student.id,status=1).count()#批准假条
        ask2_count=Ask.query.filter_by(teacher_id=teacher.id,student_id=student.id,status=2).count()#拒绝假条
        ask0_count=Ask.query.filter_by(teacher_id=teacher.id,student_id=student.id,status=0).count()#审核假条
        result={
            "student":student,
            "count":ask_count,
            "count1":ask1_count,
            "count2":ask2_count,
            "count3":ask0_count
        }
        s_lst.append(result)


    return render_template('student_ask.html',**locals())
#审核学生的假条
@csrf.exempt#单视图函数避免csrf校验
@main.route("/audit_ask/",methods=["GET","POST"])
def audit_ask():
    user_identity_id = request.cookies.get("user_identity_id")
    teacher = Teacher.query.filter_by(id=user_identity_id).first()  # 获取老师信息
    id=request.args.get("id")
    print(id)
    student=Students.query.filter_by(id=id).first()
    ask=Ask.query.filter_by(student_id=student.id,status=0)
    if request.method=='POST':
        id=request.form.get("ask_id")
        print(id)
        ask = Ask.query.filter_by(id=id).first()
        verdict=request.form.get("verdict")
        if verdict=="批准":
            ask.status = 1
            ask.save()
        else:
            ask.status = 2
            ask.save()
        return redirect('/student_ask/')
    return render_template('audit_ask.html',**locals())

#定义csrf_token错误页
#@csrf.error_handler
@main.errorhandler
@main.route('/csrf_403/')
def csrf_token_error():
    #print(reason)
    return render_template('csrf_403.html',**locals())