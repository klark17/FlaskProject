from datetime import datetime, date, time
from lessonfinder import db


lessons = db.Table('lessons',
                   db.Column('userId', db.Integer, db.ForeignKey('user.id')),
                   db.Column('lessonId', db.Integer, db.ForeignKey('lesson.id'))
                   )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer)
    lessons = db.relationship('Lesson', secondary=lessons, backref=db.backref('users', lazy='dynamic'))
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.fName}', '{self.username}', '{self.email}')"


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    organization = db.relationship('Organization', uselist=False, backref='administrator')
    # lessons = db.relationship('Lesson', backref='organizer', lazy=True)

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # classes = db.relationship('Lesson', backref='teacher', lazy=True)

    def __repr__(self):
        return f"Instructor('{self.username}', '{self.email}')"


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(30), unique=True, nullable=False)
    state = db.Column(db.String(50), unique=True, nullable=False)
    admin = db.Column(db.Integer, db.ForeignKey('admin.id'))


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False, default=date(2019, 7, 1))
    endDate = db.Column(db.DateTime, nullable=False, default=date(2019, 8, 19))
    startTime = db.Column(db.DateTime, nullable=False, default=time(6, 0, 0))
    endTime = db.Column(db.DateTime, nullable=False, default=time(7, 0, 0))
    day = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    level = db.Column(db.Integer)
    location = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(50), db.ForeignKey('instructor.id'), nullable=False)
    contactEmail = db.Column(db.String(50), db.ForeignKey('admin.id'), nullable=False)
    # registered = db.relationship('User', backref='registered_users', lazy=True)
    # for many-to-many: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

    def __repr__(self):
        return f"Lesson('{self.startDate}', '{self.endDate}', '{self.level}', '{self.location}')"
