from flask.ext.login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required
)
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash
)
from .app import app
from .models import Account
from .forms import LoginForm

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    try:
      user = Account.nodes.get(username=username)
    except Account.DoesNotExist:
        return None
    return user

@app.route('/l/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate user
        user = load_user(form.username.data)
        if (user is None) or not user.check_password(form.password.data):
            msg = 'Invalid username or password'
            if 'password' in form.errors:
                form.errors['password'].append(msg)
            else:
                form.errors['password'] = [msg]
        else:
            # All OK. Log in user.
            login_user(user)
            print('Logged in: %s' % user.username)

            return redirect(request.args.get('next') or '/')

    return render_template('login.htm', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    flash('You are now logged out.')

    return redirect(request.args.get('next') or url_for('login'))
