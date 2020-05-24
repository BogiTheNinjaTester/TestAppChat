from flask import Flask, render_template, redirect, url_for
from wtform_fields import *
from models import *

app = Flask(__name__)
app.secret_key = 'replace later'

# DB configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/ChatApplication'

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    ''' TBD '''

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data


        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('index.html', form=registration_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' TBD '''

    login_form = LoginForm()
    if login_form.validate_on_submit():
        return 'Logged in!'
    return render_template('login.html', form=login_form)

if __name__ == "__main__":

    app.run(debug=True)
