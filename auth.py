from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()  # 注意：app.py 也應該有 bcrypt = Bcrypt(app)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('帳號名稱已被使用')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        is_admin = username in ['Peggy2005', 'Peter2005']
        user = User(username=username, password_hash=hashed_password, is_approved=is_admin, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

        flash('註冊完成，等待管理員審核' if not is_admin else '管理員帳號建立成功')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            flash('帳號或密碼錯誤')
            return redirect(url_for('auth.login'))

        if not user.is_approved:
            flash('帳號尚未被管理員審核')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('登入成功')
        return redirect(url_for('home'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        if not bcrypt.check_password_hash(current_user.password_hash, current_password):
            flash('目前密碼錯誤')
            return redirect(url_for('auth.change_password'))

        current_user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        flash('密碼已更新')
        return redirect(url_for('home'))

    return render_template('change_password.html')


@auth_bp.route('/admin/approval')
@login_required
def admin_approval():
    if not current_user.is_admin:
        flash('只有管理員可以查看此頁面')
        return redirect(url_for('home'))

    pending_users = User.query.filter_by(is_approved=False).all()
    return render_template('admin_approval.html', users=pending_users)


@auth_bp.route('/admin/approve/<int:user_id>')
@login_required
def approve_user(user_id):
    if not current_user.is_admin:
        flash('只有管理員可以操作')
        return redirect(url_for('home'))

    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f'{user.username} 已通過審核')
    return redirect(url_for('auth.admin_approval'))
