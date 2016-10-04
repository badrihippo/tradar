from .app import app
import os

if 'NEO4J_REST_URL' not in os.environ:
    # Set NEO4J_REST_URL environment variable from config if unset
    # This variable is referenced by neomodel to connect to the database
    os.environ['NEO4J_REST_URL'] = app.config.get('NEO4J_REST_URL')

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

class Account(StructuredNode):
    '''
    Contains actual account data. Note that personal data is stored in
    the "Person" model instead.
    '''
    username = StringProperty(unique_index=True, required=True)
    password = StringProperty()
    email = StringProperty()

    owner = RelationshipFrom('Person', 'HAS_ACCOUNT', cardinality=One)
