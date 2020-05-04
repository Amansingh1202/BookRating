from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'userdetails'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String, nullable=False)
