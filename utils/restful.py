# Restful API
# 1. 请求方法（GET、POST）
# 2. 状态码（200,400,500）
# 3. 数据格式：JSON

from flask import jsonify


class HttpCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    permissionerror = 403
    servererror = 500


def restful_result(code,message,data):
    # 浏览器的JS中，不管请求是否成功，得到的数据都满足以下格式
    return jsonify({"code":code,"message":message,"data":{} if data is None else data})


def ok(data=None,message=""):
    return restful_result(code=HttpCode.ok,message=message,data=data)


def unauth_error(message=""):
    return restful_result(code=HttpCode.unautherror,message=message,data=None)


def params_error(message="参数错误！"):
    return restful_result(code=HttpCode.paramserror,message=message,data=None)


def server_error(message=""):
    return restful_result(code=HttpCode.servererror,message=message or '服务器内部错误',data=None)


def permission_error(message=""):
    return restful_result(code=HttpCode.permissionerror,message=message,data=None)

