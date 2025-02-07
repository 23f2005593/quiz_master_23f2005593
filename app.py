from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps
from models import db, User, Subject, Chapter, Quiz, Question, Score, create_admin
from forms import LoginForm, RegistrationForm, SubjectForm, ChapterForm, QuizForm, QuestionForm
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, migrate
from config import Config
from datetime import datetime, timedelta


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def initialize_database():
    
    pass

@app.template_filter('timeago')
def timeago(date):
    now = datetime.now(datetime.timezone.utc)
    diff = now - date

    if diff.days > 30:
        return date.strftime('%B %d, %Y')
    elif diff.days > 0:
        return f'{diff.days} days ago'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours} hours ago'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes} minutes ago'
    else:
        return 'just now'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            password=hashed_password,
            full_name=form.full_name.data,
            qualification=form.qualification.data,
            dob=form.dob.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Admin Routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    subjects = Subject.query.all()
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin_dashboard.html', subjects=subjects, users=users)

@app.route('/admin/subject/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash('Subject created!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('manage_subject.html', form=form, title='New Subject')

@app.route('/admin/chapter/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_chapter():
    form = ChapterForm()
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        chapter = Chapter(name=form.name.data, description=form.description.data, subject_id=form.subject.data)
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter created!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('manage_chapter.html', form=form, title='New Chapter')

@app.route('/admin/quiz/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_quiz():
    form = QuizForm()
    form.chapter.choices = [(c.id, c.name) for c in Chapter.query.all()]
    if form.validate_on_submit():
        quiz = Quiz(
            chapter_id=form.chapter.data,
            date_of_quiz=form.date_of_quiz.data,
            time_duration=form.time_duration.data,
            remarks=form.remarks.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('manage_quiz.html', form=form, title='New Quiz')

@app.route('/admin/question/new/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def new_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz_id,
            question_statement=form.question_statement.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added!', 'success')
        return redirect(url_for('new_question', quiz_id=quiz_id))
    return render_template('manage_question.html', form=form, quiz=quiz)

# User Routes
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    # Get total quizzes taken by user
    total_quizzes = Score.query.filter_by(user_id=current_user.id).count()
    
    # Calculate average score
    user_scores = Score.query.filter_by(user_id=current_user.id).all()
    if user_scores:
        avg_score = sum([(score.total_scored / score.total_questions) * 100 for score in user_scores]) / len(user_scores)
        avg_score = round(avg_score, 1)
    else:
        avg_score = 0
    
    # Calculate time spent (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_quizzes = Score.query.filter(
        Score.user_id == current_user.id,
        Score.timestamp >= thirty_days_ago
    ).all()
    
    total_time = 0
    for score in recent_quizzes:
        quiz_duration = score.quiz.time_duration
        if quiz_duration:
            hours, minutes = map(int, quiz_duration.split(':'))
            total_time += hours * 60 + minutes
    
    time_spent = round(total_time / 60, 1)  # Convert to hours
    
    # Get available quizzes (not attempted by user)
    attempted_quiz_ids = [score.quiz_id for score in current_user.scores]
    available_quizzes = Quiz.query.filter(~Quiz.id.in_(attempted_quiz_ids)).all()
    
    # Get subject progress
    subject_progress = []
    subjects = Subject.query.all()
    for subject in subjects:
        quiz_ids = []
        for chapter in subject.chapters:
            quiz_ids.extend([quiz.id for quiz in chapter.quizzes])
        
        subject_scores = Score.query.filter(
            Score.user_id == current_user.id,
            Score.quiz_id.in_(quiz_ids)
        ).all()
        
        if subject_scores:
            avg = sum([(score.total_scored / score.total_questions) * 100 for score in subject_scores]) / len(subject_scores)
            subject_progress.append({
                'name': subject.name,
                'avg_score': round(avg, 1)
            })
    
    # Get recent activity
    recent_activity = Score.query\
        .filter_by(user_id=current_user.id)\
        .order_by(Score.timestamp.desc())\
        .limit(4).all()

    return render_template('user_dashboard.html',
        total_quizzes=total_quizzes,
        avg_score=avg_score,
        time_spent=time_spent,
        available_quizzes=available_quizzes,
        subject_progress=subject_progress,
        recent_activity=recent_activity
    )

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    if current_user.is_admin:
        abort(403)
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    if request.method == 'POST':
        score = 0
        total = len(questions)
        for question in questions:
            selected = request.form.get(f'question_{question.id}')
            if selected and int(selected) == question.correct_option:
                score += 1
        new_score = Score(
            quiz_id=quiz.id,
            user_id=current_user.id,
            total_scored=score,
            total_questions=total
        )
        db.session.add(new_score)
        db.session.commit()
        flash(f'Quiz submitted! Your score: {score}/{total}', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('take_quiz.html', quiz=quiz, questions=questions)

@app.route('/scores')
@login_required
def scores():
    if current_user.is_admin:
        abort(403)
    scores = Score.query.filter_by(user_id=current_user.id).all()
    return render_template('scores.html', scores=scores)

if __name__ == '__main__':
    # Create database tables and admin user when the app starts
    with app.app_context():
        db.create_all()
        create_admin()
    
    app.run(debug=True)