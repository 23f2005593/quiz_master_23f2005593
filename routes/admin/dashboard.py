from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Subject, Chapter, Quiz, User, db, Score

def register_route(app):
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
    # Ensure only admins can access
            if not current_user.is_admin:
                return redirect(url_for('user_dashboard'))

            # Stats
            subjects_count = Subject.query.count()
            chapters_count = Chapter.query.count()
            quizzes_count = Quiz.query.count()
            users_count = User.query.filter_by(is_admin=False).count()  # Exclude admins if needed

            # Subject Distribution Data (e.g., number of chapters per subject)
            subjects = Subject.query.all()
            subject_data = {
                'labels': [subject.name for subject in subjects],
                'counts': [len(subject.chapters) for subject in subjects]  # Assuming Subject has a 'chapters' relationship
            }

            # Quiz Attempts Data (e.g., attempts per month)
            from datetime import datetime
            from sqlalchemy import func

            # Example: Count quiz attempts per month for the current year
            current_year = datetime.now().year
            attempts = (db.session.query(func.strftime('%Y-%m', Score.time_stamp_of_attempt), func.count(Score.id))
                        .filter(func.strftime('%Y', Score.time_stamp_of_attempt) == str(current_year))
                        .group_by(func.strftime('%Y-%m', Score.time_stamp_of_attempt))
                        .all())
            
            # Format for chart
            quiz_attempts = {
                'labels': [datetime.strptime(month, '%Y-%m').strftime('%B') for month, _ in attempts],
                'counts': [count for _, count in attempts]
            }

            # If no attempts, provide fallback data
            if not quiz_attempts['labels']:
                quiz_attempts = {
                    'labels': ['January', 'February', 'March', 'April', 'May'],
                    'counts': [0, 0, 0, 0, 0]
                }

            return render_template('admin/dashboard.html',
                                subjects_count=subjects_count,
                                chapters_count=chapters_count,
                                quizzes_count=quizzes_count,
                                users_count=users_count,
                                subject_data=subject_data,
                                quiz_attempts=quiz_attempts)