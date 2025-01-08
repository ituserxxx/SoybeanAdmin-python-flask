from flask import Blueprint
from flask_wtf import FlaskForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

from api import resp
from model.connent import db
from model.users import User

# 创建一个 Blueprint，命名为 user
auth_api = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    username = StringField('userName', validators=[DataRequired(), Length(min=1, max=80)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])


@auth_api.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() is False:
        return resp.err(form.errors)
    username = form.username.data
    password = form.password.data

    # 查询用户
    u = User.query.filter_by(username=username).first()

    if (u and check_password_hash(u.password, password)) is False:
        return resp.err('Invalid username or password')

    return resp.succ(data=u)


@auth_api.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    return resp.succ(data={"a": "111"})


@auth_api.route('/add', methods=['POST'])
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

    return {"id": new_user.id}
