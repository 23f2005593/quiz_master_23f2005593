from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Quiz, Question, Score
from datetime import datetime

def register_routes(app):
    @app.route('/user/quiz/<int:quiz_id>/view')
    @login_required
    def view_quiz(quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Check if the quiz is available based on timeframe
        now = datetime.now()
        
        # If quiz hasn't started yet, show the countdown page
        if now < quiz.start_time:
            return render_template('user/quiz_timer.html', quiz=quiz, expired=False)
        
        # If quiz has ended, show the expired page
        if now > quiz.end_time:
            return render_template('user/quiz_timer.html', quiz=quiz, expired=True)
        
        # Check if user has already taken this quiz
        previous_attempt = Score.query.filter_by(
            quiz_id=quiz.id, 
            user_id=current_user.id
        ).first()
        
        if previous_attempt:
            flash('You have already attempted this quiz!', 'info')
            # If you have a score view route, redirect there
            # return redirect(url_for('view_score', score_id=previous_attempt.id))
            # Otherwise, just show quiz info
            return render_template('user/view_quiz.html', quiz=quiz, already_taken=True)
        
        return render_template('user/view_quiz.html', quiz=quiz, already_taken=False)
    
    @app.route('/user/quiz/<int:quiz_id>/take', methods=['GET', 'POST'])
    @login_required
    def take_quiz(quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Check if the quiz is available based on timeframe
        now = datetime.now()
        
        # If quiz hasn't started yet, show the countdown page
        if now < quiz.start_time:
            return render_template('user/quiz_timer.html', quiz=quiz, expired=False)
        
        # If quiz has ended, show the expired page
        if now > quiz.end_time:
            return render_template('user/quiz_timer.html', quiz=quiz, expired=True)
        
        # # Check if user has already taken this quiz
        # previous_attempt = Score.query.filter_by(
        #     quiz_id=quiz.id, 
        #     user_id=current_user.id
        # ).first()
        
        # if previous_attempt:
        #     flash('You have already attempted this quiz!', 'info')
        #     # If you have a score view route, redirect to it
        #     # return redirect(url_for('view_score', score_id=previous_attempt.id))
        #     # Otherwise just redirect to dashboard
        #     return redirect(url_for('user_dashboard'))
        
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
            
            # Calculate percentage
            percentage = round((score / len(questions)) * 100) if questions else 0
            
            # Render the same template but with results
            return render_template('user/take_quiz.html', 
                                submitted=True, 
                                quiz=quiz, 
                                score=score, 
                                total_questions=len(questions),
                                percentage=percentage)
        
        # GET request - show the quiz form
        return render_template('user/take_quiz.html', submitted=False, quiz=quiz, questions=questions)