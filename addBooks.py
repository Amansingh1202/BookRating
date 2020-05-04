import csv
from models import *
import os
from flask import Flask

app = Flask(__name__)
os.environ['DATABASE_URL'] = 'postgres://postgres:AmansinghK1202@localhost:5432/prac'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def main():
    with open('books.csv') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                print(row)
                book = Books(isbn=row[0],title=row[1],author=row[2],year=int(row[3]))
                line_count += 1
                db.session.add(book)
                db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        main()