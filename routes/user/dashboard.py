from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Subject, Score


def register_route(app):
    @app.route('/user/dashboard')
    @login_required
    def user_dashboard():
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        
        subjects = Subject.query.all()
        recent_scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
        
        return render_template('user/dashboard.html', subjects=subjects, recent_scores=recent_scores)