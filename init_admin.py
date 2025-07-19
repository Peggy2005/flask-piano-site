from flask import Flask
from flask_bcrypt import Bcrypt
from models import db, User
from config import Config

# 初始化 Flask app
app = Flask(__name__)
app.config.from_object(Config)

# 初始化 DB & Bcrypt
db.init_app(app)
bcrypt = Bcrypt(app)

# 預設帳號資訊
admins = [
    {"username": "Peggy2005", "password": "0702"},
    {"username": "Peter2005", "password": "0413"},
]

with app.app_context():
    db.create_all()

    for admin in admins:
        # 檢查是否已存在
        existing = User.query.filter_by(username=admin["username"]).first()
        if existing:
            print(f"{admin['username']} 已存在，跳過")
            continue

        hashed_pw = bcrypt.generate_password_hash(admin["password"]).decode('utf-8')
        user = User(
            username=admin["username"],
            password_hash=hashed_pw,
            email=None,
            is_approved=True,
            is_admin=True
        )
        db.session.add(user)
        print(f"新增管理員：{admin['username']}")

    db.session.commit()
    print("初始化完成 ✅")
