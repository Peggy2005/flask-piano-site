from flask import Blueprint, render_template, request, send_from_directory
from models import Sheet
import os

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = Sheet.query.filter(
            (Sheet.title.ilike(f'%{keyword}%')) |
            (Sheet.lyrics.ilike(f'%{keyword}%')) |
            (Sheet.author.ilike(f'%{keyword}%'))
        ).all()
    return render_template('search.html', results=results)

@search_bp.route('/download/<int:id>')
def download(id):
    sheet = Sheet.query.get_or_404(id)
    filename = sheet.filename
    filepath = os.path.join('static', 'sheets')
    return send_from_directory(filepath, filename, as_attachment=True)
