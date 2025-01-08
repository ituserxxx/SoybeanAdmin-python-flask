from flask import Flask
from model.connent import db_init

# 创建 Flask 应用实例
app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:HbmimaIs...ijn@172.16.9.103:6001/soybean_admin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'flask_wtf_secret_key'  # Flask-WTF 需要一个 secret_key
app.config['WTF_CSRF_ENABLED'] = False  # 启用 CSRF 保护
db_init(app)



from api.check import check_api
from api.auth import auth_api
# 注册 api
app.register_blueprint(check_api, url_prefix='/check')
app.register_blueprint(auth_api, url_prefix='/auth')

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=9980
    )