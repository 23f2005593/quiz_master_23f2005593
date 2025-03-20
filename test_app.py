from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from database import db, migrate
from config import Config
from models import db, User, Subject, Chapter, Quiz, Question, Score
from forms import LoginForm, RegisterForm, SubjectForm, ChapterForm, QuizForm, QuestionForm

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('admin_dashboard'))
            return redirect(next_page or url_for('user_dashboard'))
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            full_name=form.full_name.data,
            qualification=form.qualification.data,
            dob=form.dob.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    subjects_count = Subject.query.count()
    chapters_count = Chapter.query.count()
    quizzes_count = Quiz.query.count()
    users_count = User.query.filter_by(is_admin=False).count()
    
    return render_template('admin/dashboard.html', 
                          subjects_count=subjects_count,
                          chapters_count=chapters_count, 
                          quizzes_count=quizzes_count,
                          users_count=users_count)

# Subject management
@app.route('/admin/subjects')
@login_required
def subjects():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@app.route('/admin/subjects/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!')
        return redirect(url_for('subjects'))
    return render_template('admin/subject_form.html', form=form, title='Add Subject')

@app.route('/admin/subjects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash('Subject updated successfully!')
        return redirect(url_for('subjects'))
    return render_template('admin/subject_form.html', form=form, title='Edit Subject')

@app.route('/admin/subjects/delete/<int:id>')
@login_required
def delete_subject(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!')
    return redirect(url_for('subjects'))

# Chapter management
@app.route('/admin/chapters')
@login_required
def chapters():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    chapters = Chapter.query.all()
    return render_template('admin/chapters.html', chapters=chapters)

@app.route('/admin/chapters/add', methods=['GET', 'POST'])
@login_required
def add_chapter():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    form = ChapterForm()
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
    
    if form.validate_on_submit():
        chapter = Chapter(
            name=form.name.data,
            description=form.description.data,
            subject_id=form.subject_id.data
        )
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter added successfully!')
        return redirect(url_for('chapters'))
    return render_template('admin/chapter_form.html', form=form, title='Add Chapter')

@app.route('/admin/chapters/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_chapter(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm(obj=chapter)
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
    
    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        chapter.subject_id = form.subject_id.data
        db.session.commit()
        flash('Chapter updated successfully!')
        return redirect(url_for('chapters'))
    return render_template('admin/chapter_form.html', form=form, title='Edit Chapter')

@app.route('/admin/chapters/delete/<int:id>')
@login_required
def delete_chapter(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    chapter = Chapter.query.get_or_404(id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully!')
    return redirect(url_for('chapters'))

# Quiz management
@app.route('/admin/quizzes')
@login_required
def quizzes():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    quizzes = Quiz.query.all()
    return render_template('admin/quizzes.html', quizzes=quizzes)

@app.route('/admin/quizzes/add/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def add_quiz(chapter_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    form = QuizForm()
    
    if form.validate_on_submit():
        quiz = Quiz(
            chapter_id=chapter.id,
            date_of_quiz=form.date_of_quiz.data,
            time_duration=form.time_duration.data,
            remarks=form.remarks.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz added successfully!')
        return redirect(url_for('edit_quiz_questions', quiz_id=quiz.id))
    
    return render_template('admin/quiz_form.html', form=form, chapter=chapter, title='Add Quiz')

@app.route('/admin/quizzes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    quiz = Quiz.query.get_or_404(id)
    form = QuizForm(obj=quiz)
    
    if form.validate_on_submit():
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.time_duration = form.time_duration.data
        quiz.remarks = form.remarks.data
        db.session.commit()
        flash('Quiz updated successfully!')
        return redirect(url_for('quizzes'))
    
    return render_template('admin/quiz_form.html', form=form, chapter=quiz.chapter, title='Edit Quiz')

@app.route('/admin/quizzes/delete/<int:id>')
@login_required
def delete_quiz(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    quiz = Quiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!')
    return redirect(url_for('quizzes'))

@app.route('/admin/quizzes/<int:quiz_id>/questions')
@login_required
def edit_quiz_questions(quiz_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return render_template('admin/quiz_questions.html', quiz=quiz, questions=questions)

@app.route('/admin/quizzes/<int:quiz_id>/questions/add', methods=['GET', 'POST'])
@login_required
def add_question(quiz_id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz.id,
            question_statement=form.question_statement.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!')
        return redirect(url_for('edit_quiz_questions', quiz_id=quiz.id))
    
    return render_template('admin/question_form.html', form=form, quiz=quiz, title='Add Question')

@app.route('/admin/questions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    question = Question.query.get_or_404(id)
    form = QuestionForm(obj=question)
    
    if form.validate_on_submit():
        question.question_statement = form.question_statement.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.correct_option = form.correct_option.data
        db.session.commit()
        flash('Question updated successfully!')
        return redirect(url_for('edit_quiz_questions', quiz_id=question.quiz_id))
    
    return render_template('admin/question_form.html', form=form, quiz=question.quiz, title='Edit Question')

@app.route('/admin/questions/delete/<int:id>')
@login_required
def delete_question(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('user_dashboard'))
    
    question = Question.query.get_or_404(id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!')
    return redirect(url_for('edit_quiz_questions', quiz_id=quiz_id))

# User routes
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get all subjects and recent scores
    subjects = Subject.query.all()
    recent_scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).limit(5).all()
    
    return render_template('user/dashboard.html', subjects=subjects, recent_scores=recent_scores)

@app.route('/user/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('user/subject.html', subject=subject)

@app.route('/user/chapter/<int:chapter_id>')
@login_required
def view_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('user/chapter.html', chapter=chapter)

@app.route('/user/quiz/<int:quiz_id>')
@login_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('user/quiz_info.html', quiz=quiz)

@app.route('/user/quiz/<int:quiz_id>/take', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    
    if not questions:
        flash('This quiz has no questions yet.')
        return redirect(url_for('view_quiz', quiz_id=quiz.id))
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_option = request.form.get(f'question_{question.id}')
            if selected_option and int(selected_option) == question.correct_option:
                score += 1
        
        # Save score
        new_score = Score(
            quiz_id=quiz.id,
            user_id=current_user.id,
            total_scored=score,
            total_questions=len(questions)
        )
        db.session.add(new_score)
        db.session.commit()
        
        flash(f'Quiz completed! Your score: {score}/{len(questions)}')
        return redirect(url_for('user_dashboard'))
    
    return render_template('user/take_quiz.html', quiz=quiz, questions=questions)

@app.route('/user/scores')
@login_required
def view_scores():
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
    return render_template('user/scores.html', scores=scores)

# API endpoints
@app.route('/api/subjects', methods=['GET'])
def api_subjects():
    subjects = Subject.query.all()
    result = []
    for subject in subjects:
        result.append({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description,
            'chapters_count': len(subject.chapters)
        })
    return {'subjects': result}

@app.route('/api/chapters/<int:subject_id>', methods=['GET'])
def api_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    result = []
    for chapter in chapters:
        result.append({
            'id': chapter.id,
            'name': chapter.name,
            'description': chapter.description,
            'quizzes_count': len(chapter.quizzes)
        })
    return {'chapters': result}

@app.route('/api/quizzes/<int:chapter_id>', methods=['GET'])
def api_quizzes(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    result = []
    for quiz in quizzes:
        result.append({
            'id': quiz.id,
            'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d'),
            'time_duration': quiz.time_duration,
            'questions_count': len(quiz.questions)
        })
    return {'quizzes': result}

if __name__ == '__main__':
    app.run(debug=True)