from flask import Flask, render_template, redirect, url_for, flash
from wtform_fields import *
from models import *
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from time import localtime, strftime

app = Flask(__name__)
app.secret_key = 'replace later'

# DB configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/ChatApplication'

db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)

socketio = SocketIO(app)
ROOMS = ['Selenium', 'Appium', 'Locust', 'Gatling']

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def index():
    ''' TBD '''

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('index.html', form=registration_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' TBD '''

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template('login.html', form=login_form)

@app.route('/chat', methods=['GET', 'POST'])
def chat():

    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))

@socketio.on('message')
def message(data):
    print(data)

    send({'msg': data['msg'], 'username': data['username'], 'timestamp':strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])

@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)
    send({'msg':data['username'] + ' has joined the ' +room + 'room'}, room=room)

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + 'has left the ' + data['room'] + 'room'}, room=data['room'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":

   socketio.run(app, debug=True)
