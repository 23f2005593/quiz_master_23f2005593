from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Chapter, Subject
from forms import ChapterForm

def register_routes(app):
    @app.route('/admin/chapters')
    @login_required
    def chapters():
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        chapters = Chapter.query.all()
        return render_template('admin/chapters.html', chapters=chapters)

    @app.route('/admin/chapters/add', methods=['GET', 'POST'])
    @login_required
    def add_chapter():
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        form = ChapterForm()
        form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
        
        if form.validate_on_submit():
            chapter = Chapter(
                name=form.name.data,
                description=form.description.data,
                subject_id=form.subject_id.data
            )
            db.session.add(chapter)
            db.session.commit()
            flash('Chapter added successfully!')
            return redirect(url_for('chapters'))
        return render_template('admin/chapter_form.html', form=form, title='Add Chapter')

    @app.route('/admin/chapters/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_chapter(id):
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        chapter = Chapter.query.get_or_404(id)
        form = ChapterForm(obj=chapter)
        form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
        
        if form.validate_on_submit():
            chapter.name = form.name.data
            chapter.description = form.description.data
            chapter.subject_id = form.subject_id.data
            db.session.commit()
            flash('Chapter updated successfully!')
            return redirect(url_for('chapters'))
        return render_template('admin/chapter_form.html', form=form, title='Edit Chapter')

    @app.route('/admin/chapters/delete/<int:id>')
    @login_required
    def delete_chapter(id):
        if not current_user.is_admin:
            flash('Access denied.')
            return redirect(url_for('user_dashboard'))
        
        chapter = Chapter.query.get_or_404(id)
        db.session.delete(chapter)
        db.session.commit()
        flash('Chapter deleted successfully!')
        return redirect(url_for('chapters'))