from .app import app
from flask.ext.login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    RelationshipTo,
    RelationshipFrom,
    
    ZeroOrMore,
    OneOrMore,
    ZeroOrOne,
    One
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
    full_name = StringProperty()

    account = RelationshipTo('Account', 'HAS_ACCOUNT', cardinality=One)
    country = RelationshipTo('Country', 'IS_FROM')

class Account(StructuredNode, UserMixin):
    '''
    Contains actual account data. Note that personal data is stored in
    the "Person" model instead.
    '''
    username = StringProperty(unique_index=True, required=True)
    password = StringProperty()
    email = StringProperty()

    owner = RelationshipFrom('Person', 'HAS_ACCOUNT', cardinality=One)

    def get_id(self):
        return self.username

    def set_password(self, plaintext):
        self.password = generate_password_hash(plaintext)

    def check_password(self, plaintext):
        if check_password_hash(self.password, plaintext):
            return True
        return False
