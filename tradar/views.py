from flask import (
    url_for,
    render_template
)
from .app import app
from .auth import (
    current_user,
    login_required
)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.htm')
    return render_template('index.htm')
