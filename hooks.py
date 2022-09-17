from flask import request, g
from flask_jwt_extended import get_jwt_identity
from models.user import OAUser
from utils import restful


def jwt_before_request():
    # 前后端分离项目中，发送真正请求之前，会先发送一个option请求，用来验证这个API是否可用
    if request.method == 'OPTION':
        return

    # http://127.0.0.1::5000：域名
    # http://127.0.0.1::5000/user/signin
    path = request.path
    # 哪些path不需要验证
    excluded_path = ('/user/signin', )
    if path in excluded_path:
        return

    identity = get_jwt_identity()
    if identity:
        user = OAUser.query.filter_by(id=identity).first()
        if user:
            # 如果有user，就绑定到全局对象g上，方便后期在其他地方使用
            setattr(g, "user", user)
    else:
        return restful.unauth_error(message='请先登录！')
