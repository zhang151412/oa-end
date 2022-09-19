from wtforms import Form
from wtforms.fields import IntegerField
from wtforms.validators import InputRequired


class ActiveStaffForm(Form):
    staff_id = IntegerField(validators=[InputRequired(message='请传入员工信息！')])
    # option:
    # 1：代表激活员工
    # 2：代表禁用员工
    option = IntegerField(validators=[InputRequired(message='请传入操作选项！')])

