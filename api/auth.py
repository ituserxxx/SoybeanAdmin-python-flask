from flask import Blueprint, request
from flask_wtf import FlaskForm
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

from api import resp
from model.connent import db
from model.users import User
from api.middleware import generate_token, generate_refresh_token, verify_refresh_token

# 创建一个 Blueprint，命名为 user
auth_api = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    userName = StringField('userName', validators=[DataRequired(), Length(min=1, max=80)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])


@auth_api.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() is False:
        return resp.err(form.errors)
    userName = form.userName.data
    password = form.password.data

    # 查询用户
    u = User.query.filter_by(userName=userName).first()

    if (u is not None and check_password_hash(u.password, password)) is False:
        return resp.err('Invalid username or password')

    return resp.succ(data={
        "token": generate_token(u.id),
        "refreshToken": generate_refresh_token(u.id)
    })


class refreshTokenForm(FlaskForm):
    refreshToken = StringField('refreshToken', validators=[DataRequired(), Length(min=1, max=120)])


@auth_api.route('/refreshToken', methods=['POST'])
def refreshToken():
    form = refreshTokenForm()
    if form.validate_on_submit() is False:
        return resp.err(form.errors)

    payload = verify_refresh_token(form.refreshToken.data)
    if payload is None:  # 假设 'valid_token' 是有效的 token
        return resp.err('message": "Invalid token')

    return resp.succ(data={
        "token": generate_token(payload['uid']),
        "refreshToken": generate_refresh_token(payload['uid'])
    })


@auth_api.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    uid = g.uid
    u = User.query.filter_by(id=uid).first()
    data = {
        "userId": u.id,
        "userName": u.userName,
        "roles": [],
        "buttons": []
    }
    return resp.succ(data)


@auth_api.route('/add', methods=['POST'])
def add():
    # 判断用户名是否已存在
    existing_user = User.query.filter_by(userName="admin").first()

    if existing_user:
        # 如果用户名已存在，返回错误信息
        return resp.succ(data="用户名已存在")
    else:
        # 用户名不存在，进行新增操作
        new_user = User(
            createBy="admin",
            createTime=datetime.utcnow(),
            userName="john_doe",
            password=generate_password_hash("123456"),
            userGender=1,
            nickName="John",
            userPhone="1234567890",
            userEmail="johndoe@example.com"
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            print("新用户添加成功")
            return resp.succ(data="新用户添加成功")
        except IntegrityError:
            db.session.rollback()
            print("数据库操作失败")
            return resp.succ(data="数据库操作失败")
