# -*- coding: utf-8 -*-
import datetime

from tsa import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Users(db.Model):
    """Table for users."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickName = db.Column(db.String(100), nullable=False)
    openId = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('USER', 'ADMIN'), default='USER')
    avatar = db.Column(db.String(255))
    lacalDateTime = db.Column(db.DateTime, default=datetime.now())
    member = db.Column(db.Integer)  # 这个是李科珂同学要求的
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        """Set password_hash."""
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        """Check password_hash validation."""
        return check_password_hash(self.password_hash, password)


class Results(db.Model):
    """Table for user's input and result of return."""
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    input = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
