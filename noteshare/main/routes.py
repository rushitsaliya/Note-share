from flask import render_template, request, Blueprint
from flask_login import login_required
from noteshare.models import Note

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/home', methods=['GET'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    filter = request.args.get('filter', None)

    if filter is None:
        notes = Note.query.order_by(Note.date_posted.desc()).paginate(page=page, per_page=5)
    elif filter == "latest":
        notes = Note.query.order_by(Note.date_posted.desc()).paginate(page=page, per_page=5)
    elif filter == "earlier":
        notes = Note.query.order_by(Note.date_posted.asc()).paginate(page=page, per_page=5)
    elif filter == "top":
        notes = Note.query.order_by(Note.ups.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', notes=notes)
