import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# 載入 .env 環境變數（Render 也可手動填）
load_dotenv()

# 初始化 Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'default-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 匯入 models 裡的 db（延遲初始化，並於下方 init_app）
from models import db, User
db.init_app(app)

# 初始化 LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# 載入使用者
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 匯入藍圖
from auth import auth_bp
from upload import upload_bp
from search import search_bp
from admin import admin_bp

# 註冊藍圖
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(search_bp)
app.register_blueprint(admin_bp)

# 首頁路由
@app.route('/')
def home():
    return render_template('home.html')

# 啟動（本地測試用）
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)