# -*- coding: utf-8 -*-
from extension import db


# 用户账号授权表
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickName = db.Column(db.String(255), nullable=False)
    openId = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    lacalDateTime = db.Column(db.String(255))

    @staticmethod
    def init_db():
        rets = [
            (1, 'test', '001', '123@123.com', '普通会员', '111', '365'),
        ]
        for ret in rets:
            users = Users()
            users.id = ret[0]
            users.nickName = ret[1]
            users.openId = ret[2]
            users.email = ret[3]
            users.type = ret[4]
            users.avatar = ret[5]
            users.lacalDateTime = ret[6]
            db.session.add(users)
        db.session.commit()
