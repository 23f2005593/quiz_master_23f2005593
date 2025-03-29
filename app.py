from flask import Flask
from flask_login import LoginManager
from datetime import datetime
from database import db, migrate
from config import Config
from models import db, User, Subject, Chapter, Quiz, Question, Score

from routes.auth.index import register_route as register_index
from routes.auth.login import register_route as register_login
from routes.auth.register import register_route as register_register
from routes.auth.logout import register_route as register_logout

from routes.admin.dashboard import register_route as register_admin_dashboard
from routes.admin.subjects import register_routes as register_admin_subjects
from routes.admin.chapters import register_routes as register_admin_chapters
from routes.admin.quizzes import register_routes as register_admin_quizzes
from routes.admin.questions import register_routes as register_admin_questions

from routes.user.dashboard import register_route as register_user_dashboard
from routes.user.subjects import register_route as register_user_subjects
from routes.user.chapters import register_route as register_user_chapters
from routes.user.quizzes import register_routes as register_user_quizzes
from routes.user.scores import register_route as register_user_scores

from routes.api.subjects import register_route as register_api_subjects
from routes.api.chapters import register_route as register_api_chapters
from routes.api.quizzes import register_route as register_api_quizzes

from routes.user.summary import register_route as register_user_summary
from routes.admin.summary import register_route as register_admin_summary

from routes.admin.users import register_routes as register_admin_users
from routes.admin.search import register_route as register_admin_search



# Add this line with the other route registrations


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

register_index(app)
register_login(app)
register_register(app)
register_logout(app)

register_admin_dashboard(app)
register_admin_subjects(app)
register_admin_chapters(app)
register_admin_quizzes(app)
register_admin_questions(app)
register_admin_summary(app)
register_admin_users(app)
register_admin_search(app)

register_user_dashboard(app)
register_user_subjects(app)
register_user_chapters(app)
register_user_quizzes(app)
register_user_scores(app)
register_user_summary(app)

register_api_subjects(app)
register_api_chapters(app)
register_api_quizzes(app)

if __name__ == '__main__':
    app.run(debug=True)