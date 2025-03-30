from flask import render_template, Blueprint, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import extract, func, desc, case, text
from models import Score, Quiz, Chapter, Subject, User, Question
from database import db
from datetime import datetime, timedelta
import calendar

admin_summary_bp = Blueprint('admin_summary', __name__)

@admin_summary_bp.route('/admin/summary')
@login_required
def admin_summary():
    if not current_user.is_admin:
        return redirect(url_for('user_dashboard'))
    
    # Total counts ko fetch karne ke liye
    total_users = User.query.filter(User.is_admin == False).count()
    total_subjects = Subject.query.count()
    total_quizzes = Quiz.query.count()
    total_questions = Question.query.count()
    total_attempts = Score.query.count()
    
    # subject-wise quiz attempts ko fetch karne ke liye
    subject_data = db.session.query(
        Subject.name,
        func.count(Score.id).label('attempts')
    ).join(Chapter, Subject.id == Chapter.subject_id)\
     .join(Quiz, Chapter.id == Quiz.chapter_id)\
     .join(Score, Quiz.id == Score.quiz_id)\
     .group_by(Subject.name)\
     .order_by(desc('attempts'))\
     .all()
    
    subjects = [item[0] for item in subject_data]
    subject_attempts = [item[1] for item in subject_data]
    
    # current year ke liye monthly attempts ko fetch karne ke liye
    current_year = datetime.now().year
    month_data = db.session.query(
        extract('month', Score.time_stamp_of_attempt).label('month'),
        func.count(Score.id).label('attempts')
    ).filter(
        extract('year', Score.time_stamp_of_attempt) == current_year
    ).group_by('month').all()
    
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    
    months = []
    monthly_attempts = []
    
    for month_num, attempts in month_data:
        months.append(month_names[int(month_num)-1])
        monthly_attempts.append(attempts)
    
    # average score ko fetch karne ke liye
    avg_scores = db.session.query(
        Subject.name,
        func.avg(Score.total_scored * 100.0 / Score.total_questions).label('avg_percentage')
    ).join(Chapter, Subject.id == Chapter.subject_id)\
     .join(Quiz, Chapter.id == Quiz.chapter_id)\
     .join(Score, Quiz.id == Score.quiz_id)\
     .group_by(Subject.name)\
     .all()
    
    avg_score_subjects = [item[0] for item in avg_scores]
    avg_score_values = [round(item[1], 2) if item[1] is not None else 0 for item in avg_scores]
    
    # last 7 days ke liye daily activity ko fetch karne ke liye
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    daily_activity = db.session.query(
        func.date(Score.time_stamp_of_attempt).label('date'),
        func.count(Score.id).label('count')
    ).filter(
        func.date(Score.time_stamp_of_attempt) >= week_ago
    ).group_by('date').all()
    
   
    activity_dates = [(today - timedelta(days=i)) for i in range(7, 0, -1)]
    activity_labels = [date.strftime('%a %d') for date in activity_dates]
    activity_counts = [0] * 7
    
    
    date_to_index = {(today - timedelta(days=i)).strftime('%Y-%m-%d'): 7-i-1 for i in range(7, 0, -1)}
    
    for date_obj, count in daily_activity:
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
            except ValueError:
                continue
        
        date_str = date_obj.strftime('%Y-%m-%d')
        if date_str in date_to_index:
            activity_counts[date_to_index[date_str]] = count
    
    performance_data = db.session.query(
        case(
            (func.avg(Score.total_scored * 100.0 / Score.total_questions) >= 90, '90-100%'),
            (func.avg(Score.total_scored * 100.0 / Score.total_questions) >= 80, '80-89%'),
            (func.avg(Score.total_scored * 100.0 / Score.total_questions) >= 70, '70-79%'),
            (func.avg(Score.total_scored * 100.0 / Score.total_questions) >= 60, '60-69%'),
            (func.avg(Score.total_scored * 100.0 / Score.total_questions) >= 50, '50-59%'),
            else_='Below 50%'
        ).label('score_range'),
        func.count(User.id).label('user_count')
    ).join(Score, User.id == Score.user_id)\
     .filter(User.is_admin == False)\
     .group_by(User.id)\
     .having(func.count(Score.id) > 0)\
     .subquery()
    
    performance_dist = db.session.query(
        performance_data.c.score_range,
        func.count().label('count')
    ).group_by(performance_data.c.score_range).all()
    
    perf_ranges = ['90-100%', '80-89%', '70-79%', '60-69%', '50-59%', 'Below 50%']
    perf_counts = [0] * len(perf_ranges)
    
    for score_range, count in performance_dist:
        if score_range in perf_ranges:
            perf_counts[perf_ranges.index(score_range)] = count
    
    return render_template(
        'admin/summary.html',
        total_users=total_users,
        total_subjects=total_subjects,
        total_quizzes=total_quizzes,
        total_questions=total_questions,
        total_attempts=total_attempts,
        subjects=subjects,
        subject_attempts=subject_attempts,
        months=months,
        monthly_attempts=monthly_attempts,
        avg_score_subjects=avg_score_subjects,
        avg_score_values=avg_score_values,
        activity_labels=activity_labels,
        activity_counts=activity_counts,
        perf_ranges=perf_ranges,
        perf_counts=perf_counts
    )

def register_route(app):
    app.register_blueprint(admin_summary_bp)