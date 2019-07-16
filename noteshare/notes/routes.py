from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from noteshare import db
from noteshare.models import Note, User
from noteshare.notes.forms import NoteForm

notes = Blueprint('notes', __name__)


@notes.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    form =  NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_note.html', title="New Note", form=form, legend="New Note")


@notes.route('/note/<int:note_id>')
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', title=note.title, note=note)


@notes.route('/note/<int:note_id>/update', methods=['GET', 'POST'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('notes.note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('create_note.html', title="Update Note", form=form, legend="Update Note")


@notes.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('main.home'))


@notes.route('/user/<string:username>')
def user_notes(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    notes = Note.query.filter_by(author=user).order_by(Note.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_notes.html', title=user.username, notes=notes, user=user)


@notes.route('/note/<int:note_id>/up', methods=['GET', 'POST'])
@login_required
def up_note(note_id):
    note = Note.query.get_or_404(note_id)
    note.ups += 1
    db.session.commit()
    from_page = request.args.get('from_page')
    return redirect(from_page) if from_page else redirect(url_for('main.home'))


@notes.route('/note/<int:note_id>/down', methods=['GET', 'POST'])
@login_required
def down_note(note_id):
    note = Note.query.get_or_404(note_id)
    note.downs += 1
    db.session.commit()
    from_page = request.args.get('from_page')
    return redirect(from_page) if from_page else redirect(url_for('main.home'))