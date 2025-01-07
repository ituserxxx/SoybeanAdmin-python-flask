from flask import Flask

from model import db_init
from api.check import check_api
from api.user import user_api

# 创建 Flask 应用实例
app = Flask(__name__)

# 注册 api
app.register_blueprint(check_api, url_prefix='/check')
app.register_blueprint(user_api, url_prefix='/user')


# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:HbmimaIs...ijn@172.16.9.103/soybean_admin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




if __name__ == '__main__':
    db_init(app)
    app.run(
        host="0.0.0.0",
        port=9980
    )