from flask import render_template, Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy import extract, func
from models import Score, Quiz, Chapter, Subject
from database import db
from datetime import datetime

summary_bp = Blueprint('user_summary', __name__)

@summary_bp.route('/user/summary')
@login_required
def summary():
    # subjects and count of quizzes attempted for each subject
    subject_data = db.session.query(
        Subject.name,
        func.count(Score.id).label('attempts')
    ).join(Chapter, Subject.id == Chapter.subject_id)\
     .join(Quiz, Chapter.id == Quiz.chapter_id)\
     .join(Score, Quiz.id == Score.quiz_id)\
     .filter(Score.user_id == current_user.id)\
     .group_by(Subject.name)\
     .all()
    
    subjects = [item[0] for item in subject_data]
    attempt_counts = [item[1] for item in subject_data]
    
    # month-wise quiz attempt data
    current_year = datetime.now().year
    month_data = db.session.query(
        extract('month', Score.time_stamp_of_attempt).label('month'),
        func.count(Score.id).label('attempts')
    ).filter(
        Score.user_id == current_user.id,
        extract('year', Score.time_stamp_of_attempt) == current_year
    ).group_by('month').all()
    
    # month numbers to names
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    
    months = []
    monthly_attempts = []
    
    for month_num, attempts in month_data:
        months.append(month_names[int(month_num)-1])
        monthly_attempts.append(attempts)
    
    return render_template(
        'user/summary.html', 
        subjects=subjects, 
        attempt_counts=attempt_counts,
        months=months,
        monthly_attempts=monthly_attempts
    )

def register_route(app):
    app.register_blueprint(summary_bp)