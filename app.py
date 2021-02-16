from models import *
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, session
import json
import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
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
    global books
    name = request.form.get('search')
    book_opt = int(request.form.get('book_opt'))
    if book_opt == 1:
        books = Books.query.filter(Books.title.like(f'%{name}%')).all()
    elif book_opt == 2:
        books = Books.query.filter(Books.isbn.like(f'%{name}%')).all()
    elif book_opt == 3:
        books = Books.query.filter(Books.author.like(f'%{name}%')).all()
    else:
        books = None
    if books == None:
        return render_template('error.html', error='No book Found,Try Again!!')
    elif books == []:
        return render_template('error.html', error='No book Found,Try Again!!')
    else:
        return render_template('review.html', books=books)


# This API returns the book details in JSON format given the ISBN number of the book
@app.route('/api/<string:isbn>', methods=['GET'])
def book_api(isbn):
    if len(isbn) != 10:
        x = {
            'Error': 'Incorrect ISBN number',
            'Status': 400
        }
        res = json.dumps(x, indent=3)
        return (res)
    elif isbn[0:8].isnumeric() == True:
        book = Books.query.filter_by(isbn=isbn).first()
        if book == None:
            x = {
                'Error': 'No book with this ISBN number',
                'Status': 400
            }
            res = json.dumps(x, indent=3)
            return (res)
        else:
            x = {
                'ISBN': book.isbn,
                'Title': book.title,
                'Author': book.author,
                'Year': book.year,
                'Average Review': book.avg_review,
                'Total Number of Ratings': book.total_rating
            }
            res = json.dumps(x, indent=3)
            return (res)
    else:
        x = {
            'Error': 'Incorrect ISBN number',
            'Status': 400
        }
        res = json.dumps(x, indent=3)
        return (res)


@app.route('/addReview', methods=['POST'])
def addReview():
    present = False
    rev = request.form.get('rate')
    book_id = request.form.get('book_id')
    user_id = session['user_id']
    reviews = Review.query.filter_by(user_id=user_id).all()
    for review in reviews:
        if review.book_id == book_id:
            present = True
    if present == False:
        review = Review(book_id=book_id, user_id=user_id, rev=rev)
        book = Books.query.filter_by(id=book_id).first()
        if book.avg_review == None:
            book.avg_review = rev
            book.total_rating = 1
            db.session.commit()
        else:
            book.avg_review = round(
                (book.total_rating * book.avg_review) / (book.total_rating + 1), 2)
            book.total_rating = book.total_rating + 1
            db.session.commit()
        db.session.add(review)
        db.session.commit()
        return render_template('success.html', message='Rating Added Successfully')
    else:
        return render_template('error.html', error='You have already submitted review for this book!!')
