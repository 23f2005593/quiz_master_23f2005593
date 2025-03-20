from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Subject
from forms import SubjectForm

def register_routes(app):
    @app.route('/admin/subjects')
    @login_required
    def subjects():
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        subjects = Subject.query.all()
        return render_template('admin/subjects.html', subjects=subjects)

    @app.route('/admin/subjects/add', methods=['GET', 'POST'])
    @login_required
    def add_subject():
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        form = SubjectForm()
        if form.validate_on_submit():
            subject = Subject(
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(subject)
            db.session.commit()
            flash('Subject added successfully!')
            return redirect(url_for('subjects'))
        return render_template('admin/subject_form.html', form=form, title='Add Subject')

    @app.route('/admin/subjects/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_subject(id):
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        subject = Subject.query.get_or_404(id)
        form = SubjectForm(obj=subject)
        if form.validate_on_submit():
            subject.name = form.name.data
            subject.description = form.description.data
            db.session.commit()
            flash('Subject updated successfully!')
            return redirect(url_for('subjects'))
        return render_template('admin/subject_form.html', form=form, title='Edit Subject')

    @app.route('/admin/subjects/delete/<int:id>')
    @login_required
    def delete_subject(id):
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        subject = Subject.query.get_or_404(id)
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!')
        return redirect(url_for('subjects'))