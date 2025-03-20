from models import Subject

def register_route(app):
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