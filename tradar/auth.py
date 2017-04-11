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
from datetime import datetime
from .app import app
from .models import Account
from .forms import (
    LoginForm,
    UsernameForm,
    PasswordForm,
)
from .util.email import (
    mail,
    Message,
)

from .util.security import ts

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

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
    form = UsernameForm()
    if form.validate_on_submit():
        # Go to next stage of login
        user = load_user(form.username.data)
        if user is None:
            # Pretend to have sent the sign-in email
            return render_template('accounts/login_emailsent.htm',
                username=form.username.data)
        elif not user.is_active:
            return render_template('accounts/login_deactivated.htm')
        elif user.signin_mode == 'password':
            password_form = PasswordForm(username=user.username)
            return render_template('accounts/login_withpassword.htm',
                form=password_form,
                name=user.owner.get().full_name)
        elif user.signin_mode == 'email':
            # Generate signin link
            data = {
                'last_login': datetime.strftime(user.last_login, DATE_FORMAT),
                'username': str(user.username),
            }
            token = ts.dumps(data, salt='login-key')
            confirm_url = url_for('login_withemail',
                token=token,
                _external=True)
            # Send the email
            msg = Message()
            msg.subject = 'Sign in to Tradar'
            msg.recipients.append(user.email)
            msg.body=render_template('emails/login_email.txt',
                name=user.username,
                confirm_url=confirm_url)
            msg.html=render_template('emails/login_email.htm',
                name=user.username,
                confirm_url=confirm_url)
            mail.send(msg)
            return render_template('accounts/login_emailsent.htm',
                name=user.username,
                confirm_url=confirm_url)
        else:
            flash('There was an error signing in. Please try again.')
    return render_template('accounts/login.htm', form=form)

@app.route('/l/email/<token>/')
def login_withemail(token):
    # Load token
    try:
        # 900 seconds = 15 minutes
        data = ts.loads(token, salt='login-key', max_age=900)
    except:
        abort(404)

    # Load user
    user = load_user(data['username'])

    # Check validity
    if user is None or user.signin_mode != 'email':
        abort(404)

    # Confirm that last_login still matches
    # If not, it means the user has already signed in,
    # in which case the token should be considered invalid.
    if datetime.strftime(user.last_login, DATE_FORMAT) != data['last_login']:
        return render_template('accounts/login_expired.htm')

    # Everything OK. Log in user.
    user.last_login = datetime.now()
    user.save()
    login_user(user)
    return redirect(request.args.get('next') or '/')


@app.route('/l/pass/', methods=['POST'])
def login_withpassword():
    form = PasswordForm()
    user = load_user(form.username.data)
    if (user is None) or not user.check_password(form.password.data):
        msg = 'Invalid password'
        if 'password' in form.errors:
            form.errors['password'].append(msg)
        else:
            form.errors['password'] = [msg]

    elif form.validate_on_submit():
        # Login and validate user
        if not user.is_active:
           return render_template('accounts/login_deactivated.htm')
        else:
            # All OK. Set last_login and login user
            user.last_login = datetime.now()
            user.save()
            login_user(user)

            return redirect(request.args.get('next') or '/')
    return render_template('accounts/login_withpassword.htm',
        form=form,
        name=user.owner.get().full_name)

@app.route('/logout/')
def logout():
    logout_user()
    flash('You are now logged out.')

    return redirect(request.args.get('next') or url_for('login'))
