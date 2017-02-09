from .app import app
from flask.ext.login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)
import uuid

from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    BooleanProperty,
    DateProperty,
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
    is_active = BooleanProperty(default=True)

    def get_id(self):
        return self.username

    def set_password(self, plaintext):
        self.password = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        if check_password_hash(self.password, plaintext):
            return True
        return False
