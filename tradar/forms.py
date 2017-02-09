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
