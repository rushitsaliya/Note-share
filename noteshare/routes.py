from noteshare import app, db, bcrypt
from noteshare.models import User, Note
from flask import render_template, url_for, flash, redirect, request
from noteshare.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

# dummy data for notes
notes = [
    {
        'id': '1',
        'author': "Rushit Saliya",
        'title': "Git Commands",
        'content': "`git log` - For showing log of commits made by different contributors in current branches."
    },
    {
        'id': '2',
        'author': "Priyank Vekariya",
        'title': "Python syntax",
        'content': "Python doesn't use semicolons (;) anymore!"
    },
    {
        'id': '3',
        'author': "Hardik Khunt",
        'title': "Django v/s Flask",
        'content': "asdf asdfa sdfjasdgoia st asdkfhas e"
    },
    {
        'id': '3',
        'author': "Divyesh Patel",
        'title': "Sublime text editor configuration",
        'content': "asdfasdf sfa df asert dafasd fast sadsad  asd g"
    },
    {
        'id': '4',
        'author': "Jenil Popat",
        'title': "VS Code extensions",
        'content': "lkasjd flkasdjr oidu c"
    },
    {
        'id': '5',
        'author': "Rushit Saliya",
        'title': "Python v/s JAVA",
        'content': "Python doesn't use semicolons (;) anymore but JAVA does!"
    },
    {
        'id': '6',
        'author': "Priyank Vekariya",
        'title': " Difference between React.js and React native",
        'content': "nasdifj sdtrse asdkt s"
    }
]

@app.route('/')
@app.route('/home')
def home():
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

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title="Account")
