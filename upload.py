import os
import boto3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Sheet, User
from config import Config

upload_bp = Blueprint('upload', __name__)

# 初始化 S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.S3_REGION
)

@upload_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        lyrics = request.form.get('lyrics', '')
        file = request.files['file']

        if not file or not file.filename.endswith('.pdf'):
            flash("請上傳 PDF 檔案")
            return redirect(url_for('upload.upload'))

        filename = secure_filename(file.filename)

        try:
            # 上傳到 S3
            s3.upload_fileobj(
                file,
                Config.S3_BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': 'application/pdf'}
            )

            # 存入資料庫
            sheet = Sheet(
                title=title,
                author=author,
                lyrics=lyrics,
                filename=filename,
                uploader_id=current_user.id
            )
            db.session.add(sheet)
            db.session.commit()
            flash("上傳成功")
            return redirect(url_for('home'))  # 可改為你的 dashboard 頁

        except Exception as e:
            print("S3 上傳失敗：", e)
            flash("上傳失敗，請稍後再試")
            return redirect(url_for('upload.upload'))

    return render_template('upload.html')
