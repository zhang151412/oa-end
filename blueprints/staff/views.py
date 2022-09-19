from flask.blueprints import Blueprint
from flask import request, g
from utils import restful
from models.user import OAUser, OACrossDepartmentAssociation
from .forms import ActiveStaffForm
from sqlalchemy import and_
from exts import db


bp = Blueprint("staff", __name__, url_prefix="/staff")


# /staff/list/2
@bp.get("/list/<int:page>")
def get_staff_list(page):
    # 谁可以获取到员工列表
    # 1. 如果只是普通员工，则不能看到员工列表
    # 2. 如果是部门leader，可以看到自己部门的所有员工
    # 3. 如果是属于董事会的，那么可以看到所有员工
    current_user = g.user
    if not current_user.is_leader and current_user.department.name != '董事会':
        return restful.permission_error(message="您没有权限获取员工列表！")

    query = None
    # 1. 如果是董事会
    if current_user.department.name == '董事会':
        query = OAUser.query
    # 2. 如果是部门领导
    else:
        query = OAUser.query.filter_by(department_id=current_user.department_id)

    # 获取总条目
    total = query.count()

    # 分页
    #一页展示10条数据
    page_size = 10
    # 第一页的范围：0-9
    # 第二页的范围：10-19
    start = (page-1)*page_size
    # a = ['a','b','c']：
    # a[1:3]=1,2
    end = start + page_size
    #切片
    query = query.slice(start, end).all()

    # 序列化
    staffs = []
    for item in query:
        staff = item.to_dict()
        staffs.append(staff)

    return restful.ok({
        "page": page,
        "total": total,
        "staffs": staffs
    })


@bp.post("/active")
def active_staff():
    # 激活和禁用员工
    form = ActiveStaffForm(request.form)
    if form.validate():
        staff_id = form.staff_id.data
        # option:
        # 1：代表激活员工
        # 2：代表禁用员工
        option = form.option.data

        current_user = g.user
        # 获取员工对象
        try:
            # get方法可以直接返回ORM模型，不像filter一样，filter是返回BaseQuery对象
            # 但是如果不存在，会抛出异常
            # get方法只接收主键
            staff = OAUser.query.get(staff_id)

            # 不能对自己进行操作
            if staff.id == current_user.id:
                return restful.params_error(message="不能对自己进行操作！")

            # 权限
            # 1. 如果是部门leader，可以操作自己部门的员工
            # 2. 如果是董事会的，可以操作自己分管的部门的所有员工
            can_do = False
            if current_user.is_leader and current_user.department_id==staff.department_id:
                can_do = True
            elif current_user.department.name == '董事会':
                # 寻找current_user分管department_id和current_user.department_id一样的
                association = OACrossDepartmentAssociation.query.filter(and_(
                    OACrossDepartmentAssociation.department_id==staff.department_id,
                    OACrossDepartmentAssociation.manager_id==current_user.id
                )).first()
                if association:
                    can_do = True

            if not can_do:
                return restful.permission_error(message="您没有权限操作此员工！")

            staff.is_active = True if option==1 else False
            db.session.commit()

            return restful.ok(data={
                "staff": staff.to_dict()
            })
        except Exception as e:
            print(e)
            return restful.params_error(message="员工不存在！")
    else:
        print(form.errors)
        return restful.params_error(message="请传入正确的参数！")
