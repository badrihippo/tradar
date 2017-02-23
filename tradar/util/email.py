from flask.ext.mail import (
    Mail,
    Message,
    email_dispatched
)
from ..app import app
mail = Mail(app)

def send_email(message, subject=None, sender=None, recipients=[]):
    '''Dummy function, to be implemented later'''
    if app.config.get('DEBUG'):
        # TODO: Implement actual email sending
        print('''
        [BEGIN EMAIL]
        From: %(sender)s
        To: %(recipients)s

        %(message)s

        [END EMAIL]
        ''' % {
            'sender': sender,
            'subject': subject,
            'message': message,
            'recipients': ', '.join([r for r in recipients])
        })
    else:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = message,
        mail.send(message)

if app.config.get('MAIL_SUPPRESS_SEND'):
    def log_message(msg, app):
        out = '\n'.join(('Sending email',
            'From: %s' % msg.sender,
            'To: %s' % ', '.join([r for r in msg.recipients]),
            'Subject: %s' % msg.subject,
            msg.body))
        app.logger.debug(out)

    email_dispatched.connect(log_message)
