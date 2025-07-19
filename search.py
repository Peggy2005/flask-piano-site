import boto3
from flask import Blueprint, render_template, request, redirect, flash
from models import Sheet
from config import Config

search_bp = Blueprint('search', __name__)

# 初始化 S3
s3 = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.S3_REGION
)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword'].strip()
        if keyword:
            results = Sheet.query.filter(
                (Sheet.title.ilike(f'%{keyword}%')) |
                (Sheet.lyrics.ilike(f'%{keyword}%')) |
                (Sheet.author.ilike(f'%{keyword}%'))
            ).all()
    return render_template('search.html', results=results)

@search_bp.route('/search/download/<int:id>')
def download(id):
    sheet = Sheet.query.get_or_404(id)

    try:
        # 產生 S3 簽名下載連結
        presigned_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': Config.S3_BUCKET_NAME,
                'Key': sheet.filename
            },
            ExpiresIn=300  # 有效時間：5 分鐘
        )
        return redirect(presigned_url)

    except Exception as e:
        print("下載失敗：", e)
        flash("下載失敗，請稍後再試")
        return redirect('/search')
