from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Quiz, Question, Score

def register_routes(app):
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