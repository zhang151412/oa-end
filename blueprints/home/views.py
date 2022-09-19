from flask.blueprints import Blueprint
from flask import request

from models.absent import OAAbsentApply
from models.user import OAUser, OADepartment
from utils import restful
from exts import db
# func中包含了数据库的聚合函数
from sqlalchemy import func

bp = Blueprint("home", __name__, url_prefix="/home")


@bp.get("/department/staff/count")
def department_staff_count():
    # 要根据部门来统计人数
    # 跨表查询
    # [('董事会', 20), ('运营部', 30),...]
    items = db.session.query(OADepartment.name, func.count(OADepartment.name)).join(OAUser).group_by(
        OADepartment.name).all()
    departments = []
    counts = []
    for item in items:
        departments.append(item[0])
        counts.append(item[1])
    return restful.ok(data={
        "departments": departments,
        "counts": counts
    })


@bp.get("/latest/absent")
def latest_absent():
    # offset,limit
    absents = OAAbsentApply.query.order_by(OAAbsentApply.create_time.desc()).limit(5).all()
    absent_dicts = []
    for absent in absents:
        item = absent.to_dict()
        item['department'] = absent.requestor.department.to_dict()
        absent_dicts.append(item)
    return restful.ok(data={
        "absents": absent_dicts
    })
