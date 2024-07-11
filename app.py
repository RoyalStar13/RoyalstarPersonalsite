from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from twilio.rest import Client
from models import User
from forms import LoginForm
import random

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Twilio configuration
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        mobile_number = form.mobile_number.data
        user = User.query.filter_by(mobile_number=mobile_number).first()
        if user is None:
            user = User(mobile_number=mobile_number)
            db.session.add(user)
            db.session.commit()
        session['mobile_number'] = mobile_number
        # Send verification code
        verification_code = random.randint(1000, 9999)
        session['verification_code'] = verification_code
        client.messages.create(
            body=f"Your verification code is {verification_code}",
            from_='+1234567890',
            to=mobile_number
        )
        return redirect(url_for('verify'))
    return render_template('index.html', form=form)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        code = request.form['code']
        if code == str(session['verification_code']):
            session['logged_in'] = True
            return redirect(url_for('chat'))
        else:
            flash('Invalid verification code')
    return render_template('verify.html')

@app.route('/chat')
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('chat.html', users=users)

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)
