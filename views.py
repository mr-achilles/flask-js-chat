import time
from flask import render_template, flash, redirect, url_for,
from flask_login import login_user, current_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send

from app import app, login
from wtform_fields import *
from models import User, db


db.create_all()
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


socketio = SocketIO(app, manage_session=False)

# Predefined hardcoded rooms for chat
# As option
ROOMS = ["lounge", "news", "games", "coding"]


@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hashing password
        hashed_pswd = pbkdf2_sha256.hash(password)
        user = User(username=username, hashed_pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route("/logout", methods=['GET'])
def logout():
    # Logout for user
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))
    return render_template("chat.html", username=current_user.username, rooms=ROOMS)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@socketio.on('incoming-msg')
def on_message(data):
    """Messages"""
    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on('join')
def on_join(data):
    """User joins room"""
    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """Leaving a room"""
    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)
