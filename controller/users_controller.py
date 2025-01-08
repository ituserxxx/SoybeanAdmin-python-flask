from flask import Blueprint
from datetime import datetime

from model.connent import db
from model.users import User
# 创建一个 Blueprint，命名为 user
user_api = Blueprint('user', __name__)

# 定义 GET 请求接口
@user_api.get("get")
def login_get():
    return {"a":"get"}

# 定义 POST 请求接口
@user_api.route('/post', methods=['POST'])
def login_post():
    return {"a":"post"}


# 定义 POST 请求接口
@user_api.route('/add', methods=['POST'])
def add():
    new_user = User(
        createBy="admin",
        createTime=datetime.utcnow(),
        userName="john_doe",
        userGender=1,
        nickName="John",
        userPhone="1234567890",
        userEmail="johndoe@example.com"
    )
    db.session.add(new_user)
    db.session.commit()

    return {"id":new_user.id}
