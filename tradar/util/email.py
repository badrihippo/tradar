from flask.ext.mail import (
    Mail,
    Message,
    email_dispatched
)
from ..app import app
mail = Mail(app)

if app.config.get('MAIL_SUPPRESS_SEND'):
    def log_message(msg, app):
        out = '\n'.join(('Sending email',
            'From: %s' % msg.sender,
            'To: %s' % ', '.join([r for r in msg.recipients]),
            'Subject: %s' % msg.subject,
            msg.body))
        app.logger.debug(out)

    email_dispatched.connect(log_message)
