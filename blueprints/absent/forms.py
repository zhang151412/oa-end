from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import InputRequired


class ApplyAbsentForm(Form):
    title = StringField(validators=[InputRequired(message="请传入请假标题！")])
    request_content = StringField(validators=[InputRequired(message="请传入请假描述！")])
    start_time = StringField(validators=[InputRequired(message="请传入起始时间！")])
    end_time = StringField(validators=[InputRequired(message="请传入结束时间！")])
    absent_type = IntegerField(validators=[InputRequired(message="请传入请假类型！")])


class HandleSubAbsentForm(Form):
    absent_id = IntegerField(validators=[InputRequired(message='请传入请假id！')])
    option = IntegerField(validators=[InputRequired(message='请传入处理结果！')])
    response_content = StringField(validators=[InputRequired(message='请传入处理理由！')])
