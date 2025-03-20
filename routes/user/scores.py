from flask import render_template
from flask_login import login_required, current_user
from models import Score

def register_route(app):
    @app.route('/user/scores')
    @login_required
    def view_scores():
        scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
        return render_template('user/scores.html', scores=scores)