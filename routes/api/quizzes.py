from models import Quiz

def register_route(app):
    @app.route('/api/quizzes/<int:chapter_id>', methods=['GET'])
    def api_quizzes(chapter_id):
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        result = []
        for quiz in quizzes:
            result.append({
                'id': quiz.id,
                'Start-Time': quiz.start_time,
                'End-Time': quiz.end_time,
                'time_duration': quiz.time_duration,
                'questions_count': len(quiz.questions)
            })
        return {'quizzes': result}