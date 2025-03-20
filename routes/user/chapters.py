from flask import render_template
from flask_login import login_required
from models import Chapter

def register_route(app):
    @app.route('/user/chapter/<int:chapter_id>')
    @login_required
    def view_chapter(chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        return render_template('user/chapter.html', chapter=chapter)