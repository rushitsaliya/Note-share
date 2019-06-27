from noteshare import app
from flask import render_template, url_for, flash, redirect
from noteshare.forms import RegistrationForm, LoginForm

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', title="Sign Up", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome, {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title="Sign In", form=form)
