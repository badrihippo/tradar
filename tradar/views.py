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
    LoginForm,
    UsernamePasswordSelectionForm,
)
from .util.security import ts
from .util.email import (
    mail,
    Message
)
from neomodel.exception import (
    UniqueProperty,
)
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

        token = ts.dumps(str(a.username), salt='email-confirm-key')
        confirm_url = url_for('signup_confirm_email',
            token=token,
            _external=True)

        msg = Message()
        msg.subject = 'Welcome to Tradar'
        msg.recipients.append(a.email)
        msg.body = render_template('emails/signup_confirm_email.txt',
            name=p.full_name,
            confirm_url=confirm_url)
        msg.html = render_template('emails/signup_confirm_email.htm',
            name=p.full_name,
            confirm_url=confirm_url)
        mail.send(msg)
        return render_template('accounts/signup_emailsent.htm', email=a.email)
    return render_template('accounts/signup.htm', form=form)

@app.route('/l/signup/activate/<token>/', methods=['GET', 'POST'])
def signup_confirm_email(token):
    try:
        # 86400 seconds = 12 hours
        username = ts.loads(token, salt='email-confirm-key', max_age=86400)
    except:
        abort(404)

    try:
        a = Account.nodes.get(username=username)
        p = a.owner.get()
    except Account.DoesNotExist:
        abort(404)

    # Abort if account is already activated
    if a.is_active or a.signin_mode != 'none':
        return redirect(url_for('index'))

    form = UsernamePasswordSelectionForm()

    if form.validate_on_submit():
        # Save data to model
        a.username = form.username.data
        if len(form.password.data) == 0:
            a.signin_mode = 'email'
        else:
            a.set_password(form.password.data)
            a.signin_mode = 'password'
        a.is_active = True

        # Try to save model
        try:
            a.save()
        except UniqueProperty:
            msg = 'That username is already taken. Please select another one.'
            form.errors['username'] = [msg]
            return render_template('accounts/signup_select_username.htm',
                form=form,
                account=a,
                person=p)

        return redirect(url_for('index'))

    # Default account setup page
    if form.username.data is None:
        form.username.data = a.username

    return render_template('accounts/signup_select_username.htm',
        form=form,
        account=a,
        person=p)

@app.route('/~<username>/')
def profile(username):
    try:
        account = Account.nodes.get(username=username)
    except Account.DoesNotExist:
        abort(404)
    person = account.owner.get()
    return render_template('profile.htm', person=person)
