from .app import app
from flask.ext.login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)
import uuid
from datetime import datetime

from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    BooleanProperty,
    DateProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
    
    ZeroOrMore,
    OneOrMore,
    ZeroOrOne,
    One
    )

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

EMAIL_OWNER_CHOICES = (
    ('me', 'me'),
    ('parents', 'my parent(s)'),
)

SIGNIN_MODE_CHOICES = (
    ('none', 'Not set'),
    ('password', 'Password'),
    ('email', 'Email'),
)

class Country(StructuredNode):
    '''
    Contains data for a particular country
    '''
    code = StringProperty(unique_index=True, required=True)
    name = StringProperty()

class Person(StructuredNode):
    '''
    Contains data for a particular person in Tradar. This is different
    from an account; even people without accounts can be referenced here.
    This is to ease account removal without breaking the data.
    '''
    uuid = StringProperty(default=lambda: uuid.uuid1())

    full_name = StringProperty(required=True)
    birthday = DateProperty()
    gender = StringProperty(choices=GENDER_CHOICES)

    account = RelationshipTo('Account', 'HAS_ACCOUNT', cardinality=One)
    country = RelationshipTo('Country', 'IS_FROM')

    profile_picture = StringProperty(default='/static/img/profile-pic-default.svg')
    cover_picture = StringProperty(default='/static/img/cover-stars.svg')

    posts = RelationshipTo('Post', 'POSTED')

class Account(StructuredNode, UserMixin):
    '''
    Contains actual account data. Note that personal data is stored in
    the "Person" model instead.
    '''
    username = StringProperty(unique_index=True, required=True)
    password = StringProperty()
    email = StringProperty()
    email_belongs_to = StringProperty()

    owner = RelationshipFrom('Person', 'HAS_ACCOUNT', cardinality=One)
    is_active = BooleanProperty(default=False)
    signin_mode = StringProperty(choices=SIGNIN_MODE_CHOICES, default='none')

    creation_date = DateTimeProperty(default=lambda: datetime.now())
    last_login = DateTimeProperty(default=lambda: datetime.now())

    def get_id(self):
        return self.username

    def set_password(self, plaintext):
        self.password = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        if check_password_hash(self.password, plaintext):
            return True
        return False

class Post(StructuredNode):
    '''
    Contains data for a single post. This model keeps track of the
    person/shop who made the post, as well as the account from which it
    was posted.
    '''

    posted_by = RelationshipFrom('Person', 'POSTED', cardinality=One)
    posting_account = RelationshipFrom('Account', 'POSTED', cardinality=One)
    date = DateTimeProperty(default=lambda: datetime.now())

    content = StringProperty()
