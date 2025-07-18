# dashboard.py

from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required, current_user
from models import Sheet

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # 查詢當前使用者上傳過的所有樂譜
    sheets = Sheet.query.filter_by(uploader_id=current_user.id).all()
    return render_template('dashboard.html', sheets=sheets)

@dashboard_bp.route('/dashboard/download/<int:id>')
@login_required
def download(id):
    # 根據樂譜 ID 下載 PDF 檔案
    sheet = Sheet.query.get_or_404(id)
    return send_from_directory('static/sheets', sheet.filename, as_attachment=True)
