from flask import (
    url_for,
    render_template
)
from .app import app

@app.route('/')
def index():
    return '<h1>Vanakkam!</h1>'
