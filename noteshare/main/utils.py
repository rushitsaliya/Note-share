from flask_mail import Message
from noteshare import mail

def send_contact_email(name, email, message):
    msg = Message('Note-Share: Contact Me', sender='noreply@demo.com', recipients=["rushitsaliya99@gmail.com"])
    
    # in the url_for() method, _external=True means generate full url rather than relative url.
    msg.body = f'''Name: {name}
Mail-Address: {email}
Message: {message}
'''
    mail.send(msg)