from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# 必须继承db.Model，以后在数据库中才能将这个模型映射成表
class OAUser(db.Model):
    __tablename__ = "oa_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jobnumber = db.Column(db.String(100), unique=True, nullable=False)
    realname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # 经过加密后的密码
    _password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    # 是否是leader
    is_leader = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        # args：是一个元组类型
        # kwargs是一个字典类型
        if "password" in kwargs:
            password = kwargs.pop("password")
            self.password = password
        super(OAUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = generate_password_hash(new_password)

    def check_password(self, raw_password):
        # check_password_hash：
        # 1. 第一个参数是经过加密后的密码
        # 2. 第二个参数是原生密码（没有经过加密的密码）
        return check_password_hash(self.password, raw_password)