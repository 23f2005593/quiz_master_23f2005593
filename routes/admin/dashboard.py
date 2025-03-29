from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Subject, Chapter, Quiz, User, db, Score
from sqlalchemy import func, or_
from datetime import datetime

def register_route(app):
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
   
            if not current_user.is_admin:
                return redirect(url_for('user_dashboard'))

          
            subjects_count = Subject.query.count()
            chapters_count = Chapter.query.count()
            quizzes_count = Quiz.query.count()
            users_count = User.query.filter_by(is_admin=False).count()  # Exclude admins if needed

            
            subjects = Subject.query.all()
            subject_data = {
                'labels': [subject.name for subject in subjects],
                'counts': [len(subject.chapters) for subject in subjects] 
            }

        
            
            current_year = datetime.now().year
            attempts = (db.session.query(func.strftime('%Y-%m', Score.time_stamp_of_attempt), func.count(Score.id))
                        .filter(func.strftime('%Y', Score.time_stamp_of_attempt) == str(current_year))
                        .group_by(func.strftime('%Y-%m', Score.time_stamp_of_attempt))
                        .all())
            
            
            quiz_attempts = {
                'labels': [datetime.strptime(month, '%Y-%m').strftime('%B') for month, _ in attempts],
                'counts': [count for _, count in attempts]
            }

            
            if not quiz_attempts['labels']:
                quiz_attempts = {
                    'labels': ['January', 'February', 'March', 'April', 'May'],
                    'counts': [0, 0, 0, 0, 0]
                }

            search_query = request.args.get('q', '')
    
            if not search_query:
                return render_template(
                    'admin/dashboard.html', 
                    search_query='',
                    subjects=[],
                    chapters=[],
                    quizzes=[],
                    users=[],
                    subjects_count=subjects_count,
                    chapters_count=chapters_count,
                    quizzes_count=quizzes_count,
                    users_count=users_count,
                    subject_data=subject_data,
                    quiz_attempts=quiz_attempts
                )
            
            # Search subjects
            subjects = Subject.query.filter(
                Subject.name.ilike(f'%{search_query}%') | 
                Subject.description.ilike(f'%{search_query}%')
            ).all()
            
            # Search chapters
            chapters = Chapter.query.filter(
                Chapter.name.ilike(f'%{search_query}%') | 
                Chapter.description.ilike(f'%{search_query}%')
            ).all()
            
            # Search quizzes
            quizzes = Quiz.query.filter(
                Quiz.remarks.ilike(f'%{search_query}%')
            ).all()
            
            # Search users
            users = User.query.filter(
                User.email.ilike(f'%{search_query}%') | 
                User.full_name.ilike(f'%{search_query}%') |
                User.qualification.ilike(f'%{search_query}%')
            ).all()    

            return render_template('admin/dashboard.html',
                                subjects_count=subjects_count,
                                chapters_count=chapters_count,
                                quizzes_count=quizzes_count,
                                users_count=users_count,
                                subject_data=subject_data,
                                quiz_attempts=quiz_attempts,
                                search_query=search_query,
                                subjects=subjects,
                                chapters=chapters,
                                quizzes=quizzes,
                                users=users)