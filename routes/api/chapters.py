from models import Chapter

def register_route(app):
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