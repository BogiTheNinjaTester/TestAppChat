from flask import Flask, render_template
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

        # check if username exists
        user_object = User.query.filter_by(username=username).all()
        if user_object:
            return 'Someone else took this name!'

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return 'User has been inserted into DB!'


    return render_template('index.html', form=registration_form)

if __name__ == "__main__":

    app.run(debug=True)
