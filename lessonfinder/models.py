from lessonfinder import db
# login_manager
from flask_user import UserMixin


# # TODO: get this to load the correct user if admin
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


lessons = db.Table('lessons',
                   db.Column('userId', db.Integer, db.ForeignKey('user.id')),
                   db.Column('lessonId', db.Integer, db.ForeignKey('lesson.id'))
                   )

organized = db.Table('organized',
                     db.Column('userId', db.Integer, db.ForeignKey('user.id')),
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
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    lessons = db.relationship('Lesson', secondary=lessons, backref=db.backref('users', lazy='dynamic'))
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    organizer = db.relationship('Lesson', backref='contactEmail', lazy='dynamic')
    organization = db.relationship('Organization', uselist=False, backref='admin')
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"User('{self.fName}', '{self.username}', '{self.email}', '{self.organization}')"


# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


# class Admin(db.Model, UserMixin):
#     __tablename__ = 'admin'
#     id = db.Column(db.Integer, primary_key=True)
#     fName = db.Column(db.String(50), nullable=False)
#     lName = db.Column(db.String(50), nullable=False)
#     username = db.Column(db.String(30), unique=True, nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     organization = db.relationship('Organization', uselist=False, backref='admin')
#     lessons = db.relationship('Lesson', backref='contactEmail', lazy='dynamic')
#     role = db.Column(db.String(10), default='admin')
#
#     def __repr__(self):
#         return f"Admin('{self.username}', '{self.fName}', '{self.lName}', '{self.email}')"


class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    lessons = db.relationship('Lesson', backref='organizer', lazy=True)
    adminId = db.Column(db.Integer, db.ForeignKey('user.id'))


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    email = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.Integer)
    location = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(50), db.ForeignKey('organization.id'), nullable=False)
    instructor = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200))
    cap = db.Column(db.Integer, nullable=False)
    # day = db.Column(db.String(10))
    # for many-to-many: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

    def __repr__(self):
        return f"Lesson('{self.startDate}', '{self.endDate}', '{self.level}', '{self.location}')"
