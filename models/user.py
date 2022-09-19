from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

# sqlalchemy_serializer：将ORM模型序列化成字典
# pip install sqlalchemy-serializer


# 必须继承db.Model，以后在数据库中才能将这个模型映射成表
class OAUser(db.Model, SerializerMixin):
    __tablename__ = "oa_user"

    # 告诉OAUser模型，需要序列化哪些字段
    serialize_only = ("id", "jobnumber", "realname", "email", "join_time", "is_active", "is_leader", "department")

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

    # 外键
    department_id = db.Column(db.Integer, db.ForeignKey("oa_department.id"))

    # user.department.name
    # department = db.relationship("OADepartment", backref="staffs")
    department = db.relationship("OADepartment",
                                 backref=db.backref("staffs", lazy="dynamic", order_by=lambda: OAUser.join_time.desc()))

    # 以后在使用user.department的时候，就会自动的使用department_id去oa_department表中寻找数据
    # 找到数据以后，生成OADepartment对象，然后赋值给user.department = OADepartment.query.get(user.department_id)

    # department.staffs

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


# 部门表
class OADepartment(db.Model,SerializerMixin):
    __tablename__ = "oa_department"

    serialize_only = ("id","name","intro")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    intro = db.Column(db.String(200))
    create_time = db.Column(db.DateTime,default=datetime.now)


# 跨部门关联表：用来存放跨部门上下级关系的
class OACrossDepartmentAssociation(db.Model, SerializerMixin):
    __tablename__ = "oa_cross_department_association"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager_id = db.Column(db.Integer, db.ForeignKey("oa_user.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("oa_department.id"))

    manager = db.relationship("OAUser",backref="associations")
    department = db.relationship("OADepartment",backref=db.backref("association",uselist=False))
