from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Question, Quiz
from forms import QuestionForm

def register_routes(app):
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