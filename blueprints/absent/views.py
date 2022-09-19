from flask import Blueprint, request, g
from models.absent import OAAbsentType, OAAbsentApply, OAAbsentStatusEnum
from models.user import OADepartment, OACrossDepartmentAssociation, OAUser
from utils import restful
from .forms import ApplyAbsentForm, HandleSubAbsentForm
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
        # 1. 如果不是部门的leader，那么responser就是所在部门的leader
        # 2. 如果是部门的leader，就要跨部门寻找responser
        # 3. 如果是董事会的leader，直接通过
        responser = None
        if not current_user.is_leader:
            # 1. filter：需要使用模型.字段来查找，查找功能更加强大（比如多个条件的时候）
            # 2. filter_by：直接使用字段，一般都是用来查找与某个字段相等的
            # 这里是要找responser，是OAUser对象，所以要从OAUser中去查找
            # OAUser.query.filter：返回的是一个BaseQuery对象
            # 如果想要获取OAUser对象，则要调用first()方法
            responser = OAUser.query.filter(and_(
                OAUser.department_id==current_user.department_id,
                OAUser.is_leader==True
            )).first()
        else:
            association = OACrossDepartmentAssociation.query.filter_by(department_id=current_user.department_id).first()
            # 如果我是董事会的leader，那么在Association表中就没有数据，所以这里要做一层判断
            if association:
                responser = association.manager
            else:
                responser = current_user

        # 请假的状态，默认情况下是等待审核
        status = OAAbsentStatusEnum.AUDITING
        # 如果responser=None，说明是董事会的leader
        # 直接将status=Pass
        if responser == current_user:
            status = OAAbsentStatusEnum.PASS

        apply_model = OAAbsentApply(
            title=title,
            request_content=request_content,
            start_time=start_time,
            end_time=end_time,
            status=status,
            absent_type_id=absent_type,
            requestor_id = requestor.id,
            responser=responser,
        )
        db.session.add(apply_model)
        db.session.commit()
        return restful.ok()
    else:
        print(form.errors)
        return restful.params_error(message="参数错误！")


# 个人请假列表
@bp.get("/my")
def my_absent():
    current_user = g.user
    absents = OAAbsentApply.query.filter_by(requestor_id=current_user.id).order_by(OAAbsentApply.create_time.desc()).all()
    absent_dicts = [item.to_dict() for item in absents]
    return restful.ok({
        "absents": absent_dicts
    })


# 下属的请假列表
@bp.get("/sub")
def sub_absent():
    current_user = g.user
    absents = OAAbsentApply.query.filter_by(responser_id=current_user.id).order_by(OAAbsentApply.create_time.desc()).all()
    absent_dicts = [item.to_dict() for item in absents]
    return restful.ok({
        "absents": absent_dicts
    })



@bp.post("/sub/handle")
def handle_sub_absent():
    form = HandleSubAbsentForm(request.form)
    if form.validate():
        absent_id = form.absent_id.data
        option = form.option.data
        response_content = form.response_content.data

        absent_model = OAAbsentApply.query.filter(and_(
            OAAbsentApply.id==absent_id,
            OAAbsentApply.responser_id==g.user.id
        )).first()

        absent_model.status = OAAbsentStatusEnum.PASS if option==1 else OAAbsentStatusEnum.REJECT
        absent_model.response_content = response_content

        db.session.commit()
        return restful.ok(data={
            'absent': absent_model.to_dict()
        })
    else:
        # {"option": ['请传入请假id！'], 'response_content': ['请传入处理理由！']}
        print(form.errors)
        return restful.params_error(message='参数上传失败！')

