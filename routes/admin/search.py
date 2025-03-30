from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from models import Subject, Chapter, Quiz, User, Question, db
from sqlalchemy import or_

admin_search_bp = Blueprint('admin_search', __name__)

@admin_search_bp.route('/admin/search')
@login_required
def admin_search():
    if not current_user.is_admin:
        return redirect(url_for('user_dashboard'))
    
    search_query = request.args.get('q', '')
    
    if not search_query:
        return render_template(
            'admin/search.html', 
            search_query='',
            subjects=[],
            chapters=[],
            quizzes=[],
            users=[],
            questions=[]

        )
    
    # subjects ko search karne ke liye
    subjects = Subject.query.filter(
        Subject.name.ilike(f'%{search_query}%') | 
        Subject.description.ilike(f'%{search_query}%')
    ).all()
    
    # chapters ko search karne ke liye
    chapters = Chapter.query.filter(
        Chapter.name.ilike(f'%{search_query}%') | 
        Chapter.description.ilike(f'%{search_query}%')
    ).all()
    
    # quizzes ko search karne ke liye
    quizzes = Quiz.query.filter(
        Quiz.remarks.ilike(f'%{search_query}%')
    ).all()
    
    # user ko search karne ke liye
    users = User.query.filter(
        User.email.ilike(f'%{search_query}%') | 
        User.full_name.ilike(f'%{search_query}%') |
        User.qualification.ilike(f'%{search_query}%')
    ).all()

    questions = Question.query.filter(
        Question.question_statement.ilike(f'%{search_query}%')
    ).all()
    
    return render_template(
        'admin/search.html',
        search_query=search_query,
        subjects=subjects,
        chapters=chapters,
        quizzes=quizzes,
        users=users,
        questions=questions
    )

def register_route(app):
    app.register_blueprint(admin_search_bp)