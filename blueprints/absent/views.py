from flask import Blueprint
from models.absent import OAAbsentType, OAAbsentApply
from utils import restful

bp = Blueprint("absent", __name__, url_prefix='/absent')


# 获取所有请请假类型
@bp.get("/type/list")
def absent_type_list():
    # absent_types：[OAAbsentType类型]
    absent_types = OAAbsentType.query.all()
    absent_type_dicts = [item.to_dict() for item in absent_types]
    # absent_type_dicts = []
    # for absent_type in absent_types:
    #     absent_type_dicts.append(absent_type.to_dict())
    return restful.ok(data={
        "types": absent_type_dicts
    })
