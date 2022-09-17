# encoding: utf-8
from flask import Flask
import config
from exts import db
from flask_migrate import Migrate
from blueprints.user.views import bp as user_bp
from blueprints.absent.views import bp as absent_bp
from flask_cors import CORS
import commands
from flask_jwt_extended import JWTManager, jwt_required
import hooks

from models.user import OAUser

# pip install flask-migrate
# 迁移三部曲
# 1. flask db init：将项目初始化成迁移仓库（只要执行一次）
# 2. flask db migrate：将ORM模型做的修改，生成迁移脚本
# 3. flask db upgrade：执行迁移脚本，将ORM的修改，真正同步到数据库中

# flask-cors：pip install flask-cors


app = Flask(__name__)
app.config.from_object(config)

# 将db与app进行绑定
db.init_app(app)
# 创建迁移对象
Migrate(app, db)
# 允许跨域
CORS(app)
# 初始化JWTManager对象
JWTManager(app)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(absent_bp)

# 注册命令
app.cli.command("greet")(commands.greet)
app.cli.command("create-user")(commands.create_user)
# 以下命令执行有顺序：[Terminal中执行：flask create-department]
# 1. create-department
# 2. create-test-user
# 3. create-association
app.cli.command("create-department")(commands.create_department)
app.cli.command("create-test-user")(commands.create_test_user)
app.cli.command("create-association")(commands.create_association)
app.cli.command("create-absent-type")(commands.create_absent_type)

# 注册钩子函数
app.before_request(jwt_required(optional=True)(hooks.jwt_before_request))


@app.route("/")
def index():
    return "后端首页1"


if __name__ == '__main__':
    app.run()
