from flask import render_template, request, Blueprint
from noteshare.models import Note

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    notes = Note.query.order_by(Note.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', notes=notes)
