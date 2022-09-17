from exts import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import enum


class OAAbsentStatusEnum(enum.Enum):
    # 审核中
    AUDITING = 1
    # 通过
    PASS = 2
    # 拒绝
    REJECT = 3


class OAAbsentType(db.Model,SerializerMixin):
    # 事假、病假、工伤假、婚假、丧假、产假、探亲假、公假、年休假
    __tablename__ = 'oa_absent_type'
    serialize_only = ('id', 'name')
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


class OAAbsentApply(db.Model,SerializerMixin):
    __tablename__ = "oa_absent_apply"

    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    request_content = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Enum(OAAbsentStatusEnum), default=OAAbsentStatusEnum.AUDITING)
    response_content = db.Column(db.Text, nullable=True)

    # 请求者
    requestor_id = db.Column(db.Integer, db.ForeignKey("oa_user.id"), nullable=False)
    responser_id = db.Column(db.Integer, db.ForeignKey("oa_user.id"), nullable=True)
    absent_type_id = db.Column(db.Integer, db.ForeignKey("oa_absent_type.id"), nullable=False)

    requestor = db.relationship("OAUser", backref="absents", foreign_keys=requestor_id)
    responser = db.relationship("OAUser", backref="sub_absents", foreign_keys=responser_id)
    absent_type = db.relationship("OAAbsentType", backref="absents")
