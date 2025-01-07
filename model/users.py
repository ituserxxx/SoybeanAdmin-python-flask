from . import db
# 创建一个模型类
class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50))
