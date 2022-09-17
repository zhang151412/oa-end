from flask.blueprints import Blueprint
from .forms import SigninForm
from flask import request
from models.user import OAUser
from flask_jwt_extended import create_access_token
from utils import restful


bp = Blueprint("user", __name__, url_prefix="/user")


# /user/signin
# GET/POST：
# GET方法：一般是用来从服务器拿数据
# POST方法：一般是用来提交数据给服务器
# 我们的这个登录，只能用post请求
@bp.post("/signin")
def signin():
    # 1. 先验证用户提交的数据是否满足格式
    # 1.1. 邮箱格式
    # 1.2. 密码：6个字符以上
    # 通过request.form可以拿到前端提交上来的数据
    # 然后传给SigninForm进行验证
    form = SigninForm(request.form)
    if form.validate():
        email = form.email.data
        password = form.password.data
        # 根据邮箱进行查找，有可能存在，有可能不存在
        user = OAUser.query.filter_by(email=email).first()
        if not user:
            return restful.params_error(message="邮箱或密码错误！")
        if not user.check_password(password):
            return restful.params_error(message="邮箱或密码错误！")
        if not user.is_active:
            return restful.params_error(message="您的账号不可用，请联系管理员！")
        # jwt pip install flask-jwt-extended
        token = create_access_token(identity=user.id)
        # 将ORM对象，转化成字典
        # OAUser(email="zhoujielun@qq.com", realname="周杰伦")
        # {"email":"zhouejilun@qq.com", "realname":"周杰伦"}
        return restful.ok(data={
            "token": token,
            "user": user.to_dict()
        })
    else:
        print(form.errors)
        return "fail"
