import json
import os

from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap

from models import *

app = Flask(__name__)
app.secret_key = 'OCML3BRawWEUeaxcuKi'
os.environ['DATABASE_URL'] = 'postgres://postgres:AmansinghK1202@localhost:5432/prac'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Bootstrap(app)


@app.route('/')
def login():
    login_error = False
    return render_template("login.html", login_error=login_error)


@app.route('/signup', methods=['POST'])
def signup():
    signup_error = False
    message = None
    return render_template("signup.html", signup_error=signup_error, message=message)


@app.route('/signupsuccess', methods=['POST'])
def signupsuccess():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template('signupsuccess.html')
    except Exception:
        err = 'Username Taken'
        return render_template('signup.html', signup_error=True, message=err)


@app.route('/index', methods=['POST'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    session['user_id'] = user.id
    print(session)
    if user.password == password:
        return render_template('index.html')
    else:
        login_error = True
        return render_template('login.html', login_error=login_error)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return render_template('login.html', login_error=None)


@app.route('/search', methods=['POST', 'GET'])
def search():
    name = request.form.get('search')
    book_opt = int(request.form.get('book_opt'))
    if book_opt == 1:
        books = Books.query.filter(Books.title.like(f'%{name}%')).all()
    elif book_opt == 2:
        books = Books.query.filter(Books.isbn.like(f'%{name}%')).all()
    elif book_opt == 3:
        books = Books.query.filter(Books.author.like(f'%{name}%')).all()
    if books == None:
        return render_template('error.html', error='No book Found,Try Again!!')
    else:
        return render_template('review.html', books=books)


@app.route('/api/<string:isbn>', methods=['GET'])
def book_api(isbn):
    books = Books.query.filter_by(isbn=isbn).first()
    x = {
        'ISBN': books.isbn,
        'Title': books.title,
        'Author': books.author,
        'Year': books.year
    }
    res = json.dumps(x, indent=3)
    return (res)
