#负责模型
from app import models
import datetime

#创建一个父类
class BaseModel(models.Model):
    __abstract__=True
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    def save(self):
        db = models.session()
        db.add(self)
        db.commit()
    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()


#创建一个用户表`
class User(BaseModel):
    __tablename__='user'
    username=models.Column(models.String(32))
    password=models.Column(models.String(32))
    identity=models.Column(models.Integer)#0是学生1是教师
    identity_id=models.Column(models.Integer,nullable=True)

#创建一个学生专业联系表
# class Stu_Cou(BaseModel):
#     __tablename__ = 'stu_cou'  # 课程学生联系表名
#     #id = models.Column(models.Integer, primary_key=True, autoincrement=True)
#     course_id=models.Column(models.Integer,models.ForeignKey('course.id'))
#     student_id = models.Column(models.Integer, models.ForeignKey('students.id'))
#学生表
class Students(BaseModel):

    __tablename__='students'#学生表名
    #id=models.Column(models.Integer,primary_key=True,autoincrement=True)#学生id
    name=models.Column(models.String(32))#学生姓名
    age=models.Column(models.Integer)#学生年龄
    gender=models.Column(models.Integer)#学生性别
    has_id=models.Column(models.Integer,nullable=True)#1是有id，0是没有id
    has_school=models.Column(models.Integer,default=1)#1是有学籍，0是没有学籍
    #与考勤表是一对多的关系
    to_attendance=models.relationship(
        'Attendance',
        backref='to_students'
    )
    #与假条表是一对多的关系
    to_ask = models.relationship(
        'Ask',
        backref='to_students'
    )


Stu_Cou=models.Table(
    "stu_cou",
    models.Column("id",models.Integer, primary_key=True, autoincrement=True),
    models.Column("course_id",models.Integer,models.ForeignKey('course.id')),
    models.Column("student_id",models.Integer, models.ForeignKey('students.id'))
)
#课程表
class Course(BaseModel):
    __tablename__ = 'course'  # 课程表名
    #id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    lable = models.Column(models.String(32))
    description = models.Column(models.Text)
    updatetime=models.Column(models.DateTime, default=datetime.timezone)
    #反向映射字段,一对多关系查询
    to_teacher=models.relationship(
        'Teacher',#映射表
        backref='to_course',#反向映射字段，通过该字段查询当表的内容
        lazy = 'dynamic'
    )
    #多对多关系查询
    to_students=models.relationship(
        'Students',
        secondary=Stu_Cou,
        backref=models.backref("to_course",lazy='dynamic'),
        lazy='dynamic'
    )

#成绩表
class Grade(BaseModel):
    __tablename__='grade'
    #id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    grade=models.Column(models.Float,default=0)#默认有的课程没有成绩
    course_id=models.Column(models.Integer,models.ForeignKey('course.id'))
    student_id=models.Column(models.Integer,models.ForeignKey('students.id'))


#考勤表
class Attendance(BaseModel):
    __tablename__ = 'attendance'
    #id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    att_time=models.Column(models.Date)
    status=models.Column(models.Integer,default=1)#0迟到1正常出勤2早退3请假4旷课
    student_id=models.Column(models.Integer,models.ForeignKey('students.id'))#考勤与学生多对一关系
 #与老师表示多对多关系
Stu_Tea = models.Table(
    "stu_tea",
    models.Column("id", models.Integer, primary_key=True, autoincrement=True),
    models.Column("teacher_id", models.Integer, models.ForeignKey('teacher.id')),
    models.Column("student_id", models.Integer, models.ForeignKey('students.id'))
)
#教师表
class Teacher(BaseModel):
    __tablename__='teacher'
    #id = models.Column(models.Integer, primary_key=True, autoincrement=True)
    name = models.Column(models.String(32))  # 老师姓名
    age = models.Column(models.Integer)  # 老师年龄
    gender = models.Column(models.Integer)  # 老师性别0男，1女，-1不知道
    description=models.Column(models.Text)#老师简介信息
    course_id=models.Column(models.Integer,models.ForeignKey('course.id'))#专业与老师一对多关系
    # 多对多关系查询
    to_students = models.relationship(
        'Students',
        secondary=Stu_Tea,
        backref=models.backref("to_teacher", lazy='dynamic'),
        lazy='dynamic'
    )
    # 与假条表是一对多的关系
    to_ask = models.relationship(
        'Ask',
        backref='to_teacher'
    )
#假条表
class Ask(BaseModel):
    __tablename__="ask"
    student_name = models.Column(models.String(32))  #请假学生姓名
    reason=models.Column(models.Text)#请假原因
    asktime = models.Column(models.DateTime)#请假时间
    subtime = models.Column(models.DateTime)#线上申请时间
    course_name=models.Column(models.String(32))#请假课程
    teacher_name=models.Column(models.String(32))#相关课程老师
    status=models.Column(models.Integer,default=0)#请假状态,0代表正在审核1代表老师批准2代表老师拒绝
    student_id = models.Column(models.Integer, models.ForeignKey('students.id'))#假条与学生是多对一关系
    teacher_id=models.Column(models.Integer, models.ForeignKey('teacher.id'))#假条与老师是多对易关系



