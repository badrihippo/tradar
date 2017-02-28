# Tradar

### The SSS social network.

Tradar is a social network specially for the SSS community to buy, sell,
and connect with each other. For more information about SSS, visit
[the SSS Wiki](http://smallsharpstones.wikia.com).

**NOTE: Work in progress!** This website is not yet completed

## Installation

To run a copy of the Tradar website on your local machine, you will
need to have Python (3.5 or similar) and a running
[neo4j](http://neo4j.com) server.

First set up the config file `instance/config.py`. (The `instance`
folder is not there; you'll have to create it). Here is an example
config file:

    DEBUG = False # set to True while testing
    SECRET_KEY = 'ABC123'
    NEO4J_REST_URL = 'bolt://username:password@localhost:7687'
    
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'me@example.com'
    MAIL_PASSWORD = 's3kr1t'
    MAIL_DEFAULT_SENDER = 'noreply@example.com'
    
    MAIL_SUPPRESS_SEND = False # set to True while testing

Next, install the Python dependencies (preferably from a
[virtualenv](http://virtualenv.readthedocs.io/)):

    pip install -r requirements.txt

And finally, use this command to run the server:

    python run.py
