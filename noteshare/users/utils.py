import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from noteshare import mail


def save_picture(form_picture):
    random_hax = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hax + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/Profile-pictures', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size, Image.ANTIALIAS)
    img.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    
    # in the url_for() method, _external=True means generate full url rather than relative url.
    msg.body = f'''To reset your password visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
Note: If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)