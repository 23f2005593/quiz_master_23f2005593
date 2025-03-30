from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_required, current_user
from models import User, db
from forms import UserForm 
# from werkzeug.security import generate_password_hash
# from datetime import datetime

admin_users_bp = Blueprint('admin_users', __name__)

@admin_users_bp.route('/admin/users')
@login_required
def users():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    # serach query ko handle karne ke liye
    search_query = request.args.get('search', '')
    
    if search_query:
        users = User.query.filter(
            (User.email.ilike(f'%{search_query}%')) | 
            (User.full_name.ilike(f'%{search_query}%')) |
            (User.qualification.ilike(f'%{search_query}%'))
        ).order_by(User.full_name).all()
    else:
        users = User.query.order_by(User.full_name).all()
    
    return render_template('admin/users.html', users=users, search_query=search_query)

@admin_users_bp.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    form = UserForm()
    
    if form.validate_on_submit():
        # email ki uniqueness ko check karne ke liye
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('admin/add_user.html', form=form)
        
        # new user ko create karne ke liye
        new_user = User(
            email=form.email.data,
            full_name=form.full_name.data,
            qualification=form.qualification.data,
            dob=form.dob.data,
            is_admin=form.is_admin.data
        )
        new_user.set_password(form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('User added successfully!', 'success')
        return redirect(url_for('admin_users.users'))
    
    return render_template('admin/add_user.html', form=form)

@admin_users_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('user_dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin_users.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.full_name} has been deleted.', 'success')
    return redirect(url_for('admin_users.users'))

def register_routes(app):
    app.register_blueprint(admin_users_bp)