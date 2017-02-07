import warnings
from flask import Flask
from neomodel import config as neoconfig
from neomodel import db

app = Flask(__name__)
try:
    app.config.from_pyfile('../instance/config.py')
except:
    warnings.warn('No config file found! Using default config')

if 'NEO4J_REST_URL' not in app.config:
    raise ValueError('Please set NEO4J_REST_URL in your config' +
        ' to connect to the database.')

neoconfig.DATABASE_URL = app.config.get('NEO4J_REST_URL')
