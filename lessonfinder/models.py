from datetime import datetime, date, time
from lessonfinder import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


lessons = db.Table('lessons',
                   db.Column('userId', db.Integer, db.ForeignKey('user.id')),
                   db.Column('lessonId', db.Integer, db.ForeignKey('lesson.id'))
                   )

organized = db.Table('organized',
                     db.Column('adminId', db.Integer, db.ForeignKey('admin.id')),
                     db.Column('lessonId', db.Integer, db.ForeignKey('lesson.id')),
                     )

hosting = db.Table('hosting',
                   db.Column('organizationId', db.Integer, db.ForeignKey('organization.id')),
                   db.Column('lessonId', db.Integer, db.ForeignKey('lesson.id')),
                   )


class User(db.Model, UserMixin):
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
    organization = db.relationship('Organization', uselist=False, backref='admin')
    lessons = db.relationship('Lesson', secondary=organized, backref=db.backref('contactEmail', lazy='dynamic'))

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    classes = db.relationship('Lesson', backref='teacher', lazy=True)

    def __repr__(self):
        return f"Instructor('{self.username}', '{self.email}')"


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(30), unique=True, nullable=False)
    state = db.Column(db.String(50), unique=True, nullable=False)
    lessons = db.relationship('Lesson', backref='organizer', lazy=True)
    adminId = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    day = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    level = db.Column(db.Integer)
    location = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(50), db.ForeignKey('organization.id'), nullable=False)
    instructor = db.Column(db.String(50), db.ForeignKey('instructor.id'), nullable=False)
    # for many-to-many: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

    def __repr__(self):
        return f"Lesson('{self.startDate}', '{self.endDate}', '{self.level}', '{self.location}')"
