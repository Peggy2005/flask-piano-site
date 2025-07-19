from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from models import User, VerificationCode

auth_bp = Blueprint('auth', __name__)  # ✅ 注意：這裡不能加句號

# 註冊
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        code = request.form['code'].strip()

        # 基本欄位檢查
        if not username or not password or not code:
            flash('所有欄位皆為必填')
            return redirect(url_for('auth.register'))

        print(f"收到註冊請求：username={username}, code={code}")

        # 檢查驗證碼
        verification = VerificationCode.query.filter_by(code=code, used=False).first()
        print("驗證碼查詢結果：", verification)

        if not verification:
            flash('驗證碼無效或已被使用')
            return redirect(url_for('auth.register'))

        # 檢查是否帳號已存在
        if User.query.filter_by(username=username).first():
            flash('帳號名稱已被使用')
            return redirect(url_for('auth.register'))

        # 建立新使用者
        hashed_password = generate_password_hash(password)
        user = User(username=username, password_hash=hashed_password)

        try:
            db.session.add(user)
            verification.used = True
            db.session.commit()
            flash('註冊成功！請登入')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print("資料庫寫入失敗：", e)
            flash('註冊失敗，請稍後再試')
            return redirect(url_for('auth.register'))

    return render_template('register.html')


# 登入
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('帳號或密碼錯誤')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('登入成功')
        return redirect(url_for('home'))

    return render_template('login.html')

# 登出
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出')
    return redirect(url_for('auth.login'))

# 修改密碼
@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        if not check_password_hash(current_user.password_hash, current_password):
            flash('目前密碼錯誤')
            return redirect(url_for('auth.change_password'))

        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('密碼已更新')
        return redirect(url_for('home'))

    return render_template('change_password.html')
