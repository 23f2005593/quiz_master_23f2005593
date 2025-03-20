from flask import render_template
from flask_login import login_required
from models import Subject

def register_route(app):
    @app.route('/user/subject/<int:subject_id>')
    @login_required
    def view_subject(subject_id):
        subject = Subject.query.get_or_404(subject_id)
        return render_template('user/subject.html', subject=subject)