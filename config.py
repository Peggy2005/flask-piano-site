import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask 核心設定
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS S3 設定（用來儲存 PDF）
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    S3_REGION = os.environ.get('S3_REGION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # 檔案上傳允許副檔名（S3 用 MIME，不用 local folder）
    ALLOWED_EXTENSIONS = {'pdf'}

    # 若同時要支援本地開發測試用（可選）
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'pdfs')
