from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Sheet

admin_sheet_bp = Blueprint('admin_sheet', __name__)

@admin_sheet_bp.route('/admin/sheets')
@login_required
def list_sheets():
    if not current_user.is_admin:
        flash('只有管理員可以查看此頁面')
        return redirect(url_for('home'))

    sheets = Sheet.query.all()
    return render_template('admin_sheets.html', sheets=sheets)

@admin_sheet_bp.route('/admin/sheets/edit/<int:sheet_id>', methods=['GET', 'POST'])
@login_required
def edit_sheet(sheet_id):
    if not current_user.is_admin:
        flash('只有管理員可以編輯')
        return redirect(url_for('home'))

    sheet = Sheet.query.get_or_404(sheet_id)

    if request.method == 'POST':
        sheet.title = request.form['title']
        sheet.author = request.form['author']
        sheet.lyrics = request.form['lyrics']
        db.session.commit()
        flash('譜已更新')
        return redirect(url_for('admin_sheet.list_sheets'))

    return render_template('edit_sheet.html', sheet=sheet)

@admin_sheet_bp.route('/admin/sheets/delete/<int:sheet_id>', methods=['POST'])
@login_required
def delete_sheet(sheet_id):
    if not current_user.is_admin:
        flash('只有管理員可以刪除')
        return redirect(url_for('home'))

    sheet = Sheet.query.get_or_404(sheet_id)
    db.session.delete(sheet)
    db.session.commit()
    flash('譜已刪除')
    return redirect(url_for('admin_sheet.list_sheets'))