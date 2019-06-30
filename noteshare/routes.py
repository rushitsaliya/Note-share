import os
import secrets
from PIL import Image
from noteshare import app, db, bcrypt
from noteshare.models import User, Note
from flask import render_template, url_for, flash, redirect, request, abort
from noteshare.forms import RegistrationForm, LoginForm, UpdateAccountForm, NoteForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    notes = Note.query.order_by(Note.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', notes=notes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Now you can Sign in to your account', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title="Sign Up", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hax = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hax + f_ext
    picture_path = os.path.join(app.root_path, 'static/Profile-pictures', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='Profile-pictures/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    form =  NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_note.html', title="New Note", form=form, legend="New Note")


@app.route('/note/<int:note_id>')
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', title=note.title, note=note)


@app.route('/note/<int:note_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('create_note.html', title="Update Note", form=form, legend="Update Note")


@app.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_notes(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    notes = Note.query.filter_by(author=user).order_by(Note.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_notes.html', title=user.username, notes=notes, user=user)