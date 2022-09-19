from flask import Blueprint,g,request
from models.finance import OAFinanceApply,OAFinanceApplyStatusEnum
from utils import restful
from sqlalchemy import and_
from models.user import OACrossDepartmentAssociation
from .forms import AddFinanceApplyForm,HandleFinanceApplyForm
from models.user import OAUser
from exts import db


bp = Blueprint("finance", __name__, url_prefix="/finance")


@bp.route("/my/list", methods=['GET'])
def my_list():
    finances = OAFinanceApply.query.filter_by(requestor_id=g.user.id).order_by(OAFinanceApply.create_time.desc())
    finance_dict_list = [finance.to_dict() for finance in finances]
    return restful.ok(data=finance_dict_list)


@bp.route("/sub/list", methods=['GET'])
def sub_list():
    finances = OAFinanceApply.query.filter_by(responser_id=g.user.id).order_by(OAFinanceApply.create_time.desc()).all()
    return restful.ok(data=[finance.to_dict() for finance in finances])


@bp.post("/add")
def add_finance():
    form = AddFinanceApplyForm(request.form)
    if form.validate():
        title = form.title.data
        request_content = form.request_content.data
        money = form.money.data

        responser = None
        if not g.user.is_leader:
            responser = OAUser.query.filter(and_(
                OAUser.department == g.user.department,
                OAUser.is_leader == True
            )).first()
        else:
            associtaion = OACrossDepartmentAssociation.query.filter_by(department=g.user.department).first()
            if associtaion:
                responser = associtaion.manager

        finance = OAFinanceApply(
            title = title,
            request_content = request_content,
            money = money,
            requestor = g.user,
            responser = responser
        )
        if not responser:
            finance.status = OAFinanceApplyStatusEnum.PASS
        db.session.add(finance)
        db.session.commit()
        return restful.ok(data=finance.to_dict())
    else:
        print(form.errors)
        return restful.params_error()


@bp.post("/approval")
def handle_finance_apply():
    form = HandleFinanceApplyForm(request.form)
    if form.validate():
        finance_id = form.finance.data
        responser_content = form.response_content.data
        result = form.option.data
        user = g.user

        finance = OAFinanceApply.query.get(finance_id)
        if finance.responser.id != user.id:
            return restful.params_error("您不是该财务的审批者！")

        finance.response_content = responser_content
        finance.status = OAFinanceApplyStatusEnum.PASS if result==1 else OAFinanceApplyStatusEnum.REJECT
        db.session.commit()

        finance_dict = finance.to_dict()
        return restful.ok(data=finance_dict)
    else:
        print(form.errors)
        return restful.params_error()
