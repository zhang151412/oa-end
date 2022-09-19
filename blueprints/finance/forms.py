from wtforms import Form
from wtforms.fields import StringField, IntegerField, DecimalField
from wtforms.validators import InputRequired


class AddFinanceApplyForm(Form):
    title = StringField(validators=[InputRequired(message="请传入财务申请标题！")])
    request_content = StringField(validators=[InputRequired(message="请传入财务申请描述！")])
    money = DecimalField(validators=[InputRequired(message="请输入申请金额！")])


class HandleFinanceApplyForm(Form):
    # 审核财务申请表单
    finance = IntegerField(validators=[InputRequired(message='请输入申请ID！')])
    response_content = StringField(validators=[InputRequired(message='请输入反馈意见！')])
    option = IntegerField(validators=[InputRequired(message='请输入审批结果！')])
