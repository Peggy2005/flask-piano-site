from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/approve_users')
@login_required
def approve_users():
    if not current_user.is_admin:
        flash("你沒有權限進入這個頁面")
        return redirect(url_for('home'))

    pending_users = User.query.filter_by(is_approved=False, is_admin=False).all()
    return render_template('approve_users.html', users=pending_users)

@admin_bp.route('/approve/<int:user_id>')
@login_required
def approve_user(user_id):
    if not current_user.is_admin:
        flash("你沒有權限進行此操作")
        return redirect(url_for('home'))

    user = User.query.get(user_id)
    if user:
        user.is_approved = True
        db.session.commit()
        flash(f"已批准使用者 {user.username}")
    return redirect(url_for('admin.approve_users'))
