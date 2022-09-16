from wtforms import Form
from wtforms.fields import StringField
# pip install email_validator
from wtforms.validators import Email, Length


class SigninForm(Form):
    email = StringField(validators=[Email(message="邮箱格式不满足！")])
    password = StringField(validators=[Length(min=6, max=20, message="密码长度必须在6-20之间！")])

