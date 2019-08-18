#表单校验，类创建
import wtforms #定义字段
from flask_wtf import FlaskForm #定义表单
from wtforms import validators  #定义校验
from app.models import *

#因为教师与专业是多对一的关系，所以实用查询返回所有的课程
#course_list=[(c.id,c.lable) for c in Course.query.all()]
course_list=[]

class TeacherForm(FlaskForm):
    """
    form字段的参数
    label=None, 表单的标签
    validators=None, 校验，传入校验的方法
    filters=tuple(), 过滤
    description='',  描述
    id=None, html id
    default=None, 默认值
    widget=None,
    render_kw=None,
    """
    name = wtforms.StringField("教师姓名",
                               render_kw={
                                   "class":"form-control",
                                   "placeholder":"教师姓名"
                               },
                               validators=[
                                   validators.DataRequired("姓名不可以为空")
                               ]

                               )
    age=wtforms.IntegerField("教师年龄",
                             render_kw={
                                  "class":"form-control",
                                   "placeholder":"教师年龄"
                             },
                             validators=[
                                 validators.DataRequired("年龄不可以为空")
                             ]
                             )
    gender = wtforms.SelectField(
        "性别",
        choices=[
            ("1", "男"),
            ("2", "女")
        ],
        render_kw={
            "class": "form-control",
        }
    )
    course = wtforms.SelectField(
        "学科",
        choices=[
            ("1",'PYTHON'),
            ("2", 'JAVA'),
            ("3", 'UI'),
            ("4", 'WEB'),

        ],
        #choices=course_list,
        render_kw={
            "class":"form-control"
        }
    )
#学生和考勤是一对多系
class StudentsForm(FlaskForm):
    name = wtforms.StringField("学生姓名",
                               render_kw={
                                   "class": "form-control",
                                   "placeholder": "学生姓名"
                               },
                               validators=[
                                   validators.DataRequired("姓名不可以为空")
                               ]

                               )
    age = wtforms.IntegerField("学生年龄",
                               render_kw={
                                   "class": "form-control",
                                   "placeholder": "学生年龄"
                               },
                               validators=[
                                   validators.DataRequired("年龄不可以为空")
                               ]
                               )
    gender = wtforms.SelectField(
        "性别",
        choices=[
            ("1", "男"),
            ("2", "女")
        ],
        render_kw={
            "class": "form-control",
        },

    )
    has_id = wtforms.SelectField(
        "是否有id",
        choices=[
            ("0", "没有学生id号码"),
            ("1", "有学生id号码")
        ],
        render_kw={
            "class": "form-control",

        }
    )

