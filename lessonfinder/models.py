from lessonfinder import db
from flask_user import UserMixin


lessons = db.Table('lessons',
                   db.Column('participantId', db.Integer, db.ForeignKey('participant.id')),
                   db.Column('userParticipantId', db.Integer, db.ForeignKey('user.id')),
                   db.Column('lessonId', db.Integer, db.ForeignKey('lesson.id'))
                   )

hosting = db.Table('hosting',
                   db.Column('organizationId', db.Integer, db.ForeignKey('organization.id')),
                   db.Column('lessonId', db.Integer, db.ForeignKey('lesson.id')),
                   )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False)
    fName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    lessons = db.relationship('Lesson', secondary=lessons, backref=db.backref('selfParticipant', lazy='dynamic'))
    dependents = db.relationship('Participant', backref=db.backref('guardian'))

    # organization = db.relationship('Organization', uselist=False, backref='admin')
    # roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    # active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    # organizer = db.relationship('Lesson', backref='contactEmail', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.fName}', '{self.username}', '{self.email}')"


class Participant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)
    contactNum = db.Column(db.String(12))
    contactEmail = db.Column(db.String(50), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    lessons = db.relationship('Lesson', secondary=lessons, backref=db.backref('participants', lazy='dynamic'))


    def __repr__(self):
        return f"Dependent('{self.fName}', '{self.contactNum}', '{self.contactEmail}')"


class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    manager = db.Column(db.String(50), nullable=False)
    managerEmail = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    lessons = db.relationship('Lesson', backref='organization', lazy=True)


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    contactEmail = db.Column(db.String(250), nullable=False)
    level = db.Column(db.Integer)
    location = db.Column(db.String(50), nullable=False)
    organizationId = db.Column(db.Integer(), db.ForeignKey('organization.id'), nullable=False)
    instructor = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200))
    cap = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Lesson('{self.startDate}', '{self.endDate}', '{self.level}', '{self.location}')"
