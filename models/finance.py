from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
import enum

class OAFinanceApplyStatusEnum(enum.Enum):
    # 审核中
    AUDITING = 1
    PASS = 2
    REJECT = 3


class OAFinanceApply(db.Model, SerializerMixin):
    __tablename__ = 'oa_finance_apply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    request_content = db.Column(db.Text, nullable=True)
    money = db.Column(db.DECIMAL, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Enum(OAFinanceApplyStatusEnum), default=OAFinanceApplyStatusEnum.AUDITING)
    response_content = db.Column(db.Text, nullable=True)

    # 请求者
    requestor_id = db.Column(db.Integer,db.ForeignKey("oa_user.id"), nullable=False)
    responser_id = db.Column(db.Integer,db.ForeignKey("oa_user.id"), nullable=True)

    requestor = db.relationship("OAUser", backref="finances", foreign_keys=requestor_id)
    responser = db.relationship("OAUser", backref="sub_finances", foreign_keys=responser_id)
