from flask import (
    url_for,
    render_template,
    abort,
)
from .app import app
from .auth import (
    current_user,
    login_required
)
from .models import (
    Country,
    Account,
    Person
)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.htm')
    return render_template('index.htm')

@app.route('/~<username>/')
def profile(username):
    try:
        account = Account.nodes.get(username=username)
    except Account.DoesNotExist:
        abort(404)
    person = account.owner.get()
    return render_template('profile.htm', person=person)
