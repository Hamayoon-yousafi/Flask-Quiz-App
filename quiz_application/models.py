from . import db 
from flask_login import UserMixin  
from datetime import datetime

user_subject = db.Table('user_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE')),
    db.Column('date_enrolled', db.DateTime, default=datetime.now())
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(30), default="Pending") 
    subjects = db.relationship("Subject", secondary=user_subject, passive_deletes=True, cascade="all, delete") 
    marks = db.relationship("Mark", backref="marks", single_parent=True, cascade="all, delete") 


class Subject(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    about = db.Column(db.String(150))
    users = db.relationship("User", secondary=user_subject, passive_deletes=True, cascade="all, delete")
    questions = db.relationship('Question', backref="subject", cascade="all, delete") 
    manager_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150), unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"))
    choice_one = db.Column(db.String(150))
    choice_two = db.Column(db.String(150))
    choice_three = db.Column(db.String(150))
    answer = db.Column(db.String(150))
    manager_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_marks = db.Column(db.String(150))
    quiz_taken_date = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
