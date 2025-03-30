from flask import render_template
from flask_login import login_required, current_user
from models import Score

def register_route(app):
    @app.route('/user/scores')
    @login_required
    def view_scores():
        scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
        print(f"Found {len(scores)} scores for user {current_user.id}")
        # score ko debug karne ke liye
        if scores:
            print(f"First score: {scores[0].total_scored}/{scores[0].total_questions}")
            print(f"Quiz chapter: {scores[0].quiz.chapter.name if hasattr(scores[0].quiz, 'chapter') else 'No chapter'}")
        return render_template('user/scores.html', scores=scores)