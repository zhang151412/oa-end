from flask.blueprints import Blueprint
from .forms import SigninForm
from flask import request

bp = Blueprint("user", __name__, url_prefix="/user")


# /user/signin
# GET/POST：
# GET方法：一般是用来从服务器拿数据
# POST方法：一般是用来提交数据给服务器
# 我们的这个登录，只能用post请求
@bp.route("/signin", methods=["POST"])
def signin():
    # 1. 先验证用户提交的数据是否满足格式
    # 1.1. 邮箱格式
    # 1.2. 密码：6个字符以上
    # 通过request.form可以拿到前端提交上来的数据
    # 然后传给SigninForm进行验证
    form = SigninForm(request.form)
    if form.validate():
        return "表单验证成功！"
    else:
        print(form.errors)
        return "fail"
