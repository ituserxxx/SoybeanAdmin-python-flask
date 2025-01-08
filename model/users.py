from datetime import datetime

from model.connent import db


class User(db.Model):
    __tablename__ = 'users'  # 表名

    # 定义字段与类型
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    createBy = db.Column(db.String(100), nullable=False, comment='创建人')
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, comment='创建时间')
    updateBy = db.Column(db.String(100), default=None, comment='更新人')
    updateTime = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow, comment='更新时间')
    status = db.Column(db.Boolean, default=True, comment='状态（1 启用，0 禁用）')
    userName = db.Column(db.String(50), nullable=False, comment='用户名')
    userGender = db.Column(db.Boolean, default=0, comment='性别（0 未知，1 男，2 女）')
    nickName = db.Column(db.String(100), default=None, comment='昵称')
    userPhone = db.Column(db.String(20), default=None, comment='用户电话')
    userEmail = db.Column(db.String(100), default=None, comment='用户邮箱')
