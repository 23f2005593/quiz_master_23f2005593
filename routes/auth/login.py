from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user
from models import User
from forms import LoginForm

def register_route(app):
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