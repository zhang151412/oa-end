# encoding: utf-8
from flask import Flask
import config
from exts import db
from flask_migrate import Migrate
from blueprints.user.views import bp as user_bp
from flask_cors import CORS

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

# 注册蓝图
app.register_blueprint(user_bp)


@app.route("/")
def index():
    return "后端首页1"


if __name__ == '__main__':
    app.run()
