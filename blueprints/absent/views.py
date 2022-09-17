from flask import Blueprint, request, g
from models.absent import OAAbsentType, OAAbsentApply, OAAbsentStatusEnum
from models.user import OADepartment, OACrossDepartmentAssociation, OAUser
from utils import restful
from .forms import ApplyAbsentForm
from datetime import datetime
from sqlalchemy import and_
from exts import db


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


# 提交请假申请
@bp.post("/apply")
def apply_absent():
    form = ApplyAbsentForm(request.form)
    if form.validate():
        title = form.title.data
        request_content = form.request_content.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        absent_type = form.absent_type.data

        # 将start_time和end_time从字符串转化为时间类型(DateTime)
        # 2022年12月12日，2022-09-17
        start_time = datetime.strptime(start_time, "%Y-%m-%d")
        end_time = datetime.strptime(end_time, "%Y-%m-%d")

        current_user = g.user
        requestor = current_user

        # 审核的用户
        # 1. 如果不是部门的leader，那么responsor就是所在部门的leader
        # 2. 如果是部门的leader，就要跨部门寻找responsor
        # 3. 如果是董事会的leader，直接通过
        responsor = None
        if not current_user.is_leader:
            # 1. filter：需要使用模型.字段来查找，查找功能更加强大（比如多个条件的时候）
            # 2. filter_by：直接使用字段，一般都是用来查找与某个字段相等的
            # 这里是要找responsor，是OAUser对象，所以要从OAUser中去查找
            responsor = OAUser.query.filter(and_(
                OAUser.department_id==current_user.department_id,
                OAUser.is_leader==True
            )).first()
        else:
            association = OACrossDepartmentAssociation.query.filter_by(department_id=current_user.department_id).first()
            # 如果我是董事会的leader，那么在Association表中就没有数据，所以这里要做一层判断
            if association:
                responsor = association.manager

        # 请假的状态，默认情况下是等待审核
        status = OAAbsentStatusEnum.AUDITING
        # 如果 responsor = None，说明是董事会的leader
        # 直接将status=Pass
        if not responsor:
            status = OAAbsentStatusEnum.PASS

        apply_model = OAAbsentApply(
            title=title,
            request_content=request_content,
            start_time=start_time,
            end_time=end_time,
            requestor=requestor,
            status=status,
            responser=responsor,
            absent_type_id=absent_type
        )
        db.session.add(apply_model)
        db.session.commit()
        return restful.ok()
    else:
        print(form.errors)
        return restful.params_error(message="参数错误！")

