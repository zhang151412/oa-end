from datetime import timedelta
# 1.修改完代码后会自动加载程序
# 2.
DEBUG = True

#
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_USERNAME = "root"
DB_PASSWORD = "1234"
DB_DATABASE = "oa_course"


SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 设置flask的加密盐
SECRET_KEY = "dfasfjsadfjsdkfjsd"

# 设置jwt token过期时间
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)


