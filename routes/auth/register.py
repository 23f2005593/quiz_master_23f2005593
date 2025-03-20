from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from models import User, db
from forms import RegisterForm

def register_route(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                full_name=form.full_name.data,
                qualification=form.qualification.data,
                dob=form.dob.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        return render_template('auth/register.html', form=form)