
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Quiz, Chapter
from forms import QuizForm
from datetime import datetime

def register_routes(app):
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
                start_time=form.start_time.data,
                end_time=form.end_time.data,
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
            quiz.start_time = form.start_time.data
            quiz.end_time = form.end_time.data
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