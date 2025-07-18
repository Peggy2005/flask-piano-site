from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)  # 用戶名稱（不能改）
    password_hash = db.Column(db.String(128), nullable=False)  # 儲存 hash 後的密碼
    email = db.Column(db.String(120), unique=True)  # 可選：加 email
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)  # 一次性使用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # 歌曲名稱
    author = db.Column(db.String(100), nullable=False)  # 作者
    lyrics = db.Column(db.Text)  # 歌詞（可用於搜尋）
    filename = db.Column(db.String(200), nullable=False)  # PDF 檔名（實際儲存用）
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 上傳者 ID
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    uploader = db.relationship('User', backref='sheets')
