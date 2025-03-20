from flask import render_template

def register_route(app):
    @app.route('/')
    def index():
        return render_template('index.html')