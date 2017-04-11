from flask.ext.wtf import Form
from wtforms import (
    TextField,
    TextAreaField,
    PasswordField,
    SelectField,
    RadioField,
    IntegerField,
    DateField,
    BooleanField,
    HiddenField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import (
    Required,
    Email,
    Length,
    NumberRange,
)
from .models import (
    EMAIL_OWNER_CHOICES,
    Account
)
GENDER_CHOICES = (
    ('F', 'girl'),
    ('M', 'boy'),
    ('O', '(other)'),
)

class LoginForm(Form):
    username= TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class UsernameForm(Form):
    username = TextField('Username', validators=[Required()])

class PasswordForm(Form):
    username= HiddenField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class UsernamePasswordSelectionForm(Form):
    username = TextField('Username', validators=[])
    password = PasswordField('Password', validators=[])

    def validate_password(form, field):
        if len(field.data) < 6 and len(field.data) != 0:
            raise ValidationError('Password must be at least 6 characters (unless it\'s blank)')


class SignupForm(Form):
    name = TextField('Name', validators=[Required()])
    birthday = DateField('Birthday', validators=[Required()])
    gender = SelectField('Gender',
        choices=GENDER_CHOICES,
        validators=[Required()])
    email = TextField('Email', validators=[Required(), Email()])
    email_belongs_to = SelectField('Email belongs to',
        choices=EMAIL_OWNER_CHOICES,
        validators=[Required()])
    accepted_terms = BooleanField('I agree to the Terms and Conditions',
        validators=[Required()])

POST_SHARE_CHOICES = (
    ('public', 'All SSSians'),
)

class NewPostForm(Form):
    posted_by = HiddenField('Post author')
    content = TextAreaField('Post Content', validators=[Required()])
    share_with = SelectField(choices=POST_SHARE_CHOICES)
    submit_button = SubmitField('Post')
