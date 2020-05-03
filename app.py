from flask import Flask, render_template,request
import os
from models import *

app = Flask(__name__)
os.environ['DATABASE_URL'] = 'postgres://postgres:AmansinghK1202@localhost:5432/prac'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def login():
    login_error = False
    return render_template("login.html",login_error = login_error)

@app.route('/signup',methods=['POST'])
def signup():
    signup_error = False
    message = None
    return render_template("signup.html",signup_error = signup_error,message=message)

@app.route('/signupsuccess',methods=['POST'])
def signupsuccess():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('passwword')
    user1 = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(email=email).first()
    if user1 == None and user2 == None:
        user = User(username=username,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return render_template('signupsuccess.html')
    else:
        signup_error = True
        if user1 != None:
            err = 'Username Taken'
        elif user2 != None:
            err = 'Email Taken'
        elif user1 != None and user2 != None:
            err = 'Username and email taken'
        else:
            err = None
        return render_template('signup.html',signup_error = signup_error,message = err)

@app.route('/index',methods=['POST'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user.password == password:
        return render_template('index.html')
    else:
        login_error = True
        return render_template('login.html',login_error = login_error)