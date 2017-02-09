from flask.ext.wtf import Form
from wtforms import (
    TextField,
    PasswordField,
    SelectField,
    RadioField,
    IntegerField,
    DateField,
    BooleanField,
)
from wtforms.validators import (
    Required,
    Email,
    Length,
    NumberRange,
)
from .models import (
    EMAIL_OWNER_CHOICES,
)
GENDER_CHOICES = (
    ('F', 'girl'),
    ('M', 'boy'),
    ('O', '(other)'),
)

class LoginForm(Form):
    username= TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

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
