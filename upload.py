import os
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Sheet

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'static/sheets'

@upload_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        lyrics = request.form.get('lyrics', '')
        file = request.files['file']

        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(save_path)

            sheet = Sheet(title=title, author=author, lyrics=lyrics, filename=filename, uploader=current_user)
            db.session.add(sheet)
            db.session.commit()
            return redirect(url_for('search.search'))

    return render_template('upload.html')