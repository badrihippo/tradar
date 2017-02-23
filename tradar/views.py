from flask import (
    url_for,
    redirect,
    render_template,
    abort,
    flash,
)
from .app import (
    app,
    db,
)
from .auth import (
    current_user,
    login_required
)
from .models import (
    Country,
    Account,
    Person
)
from .forms import (
    SignupForm,
)
from .util.security import ts
from .util.email import send_email
import uuid

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.htm')
    return render_template('index.htm')

@app.route('/l/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        with db.transaction:
            p = Person()
            a = Account()
            a.username = uuid.uuid1()
            a.email = form.email.data
            a.email_belongs_to = form.email_belongs_to.data
            p.full_name = form.name.data
            p.gender = form.gender.data
            p.birthday = form.birthday.data
            a.save()
            p.save()
        p.account.connect(a)
        msg = 'Please go to the following link to sign up: %s' % '<...>'
        send_email(msg, sender='noreply@tradar', recipients=[form.email.data])
        flash('Please check your inbox for signup instructions')
        return redirect(url_for('index'))
    return render_template('signup.htm', form=form)

@app.route('/~<username>/')
def profile(username):
    try:
        account = Account.nodes.get(username=username)
    except Account.DoesNotExist:
        abort(404)
    person = account.owner.get()
    return render_template('profile.htm', person=person)
