from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, \
    DateTimeField, IntegerField, DateField, TimeField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from wtforms_components import TimeField, DateField
from flask_user import current_user
from lessonfinder.models import User


levels = [('None', 'None'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')]
days = [('None', 'None'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                  ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                  ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]


class SignupForm(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired()])
    lName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Choose another.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    location = StringField('Location')
    organization = StringField('Organization')
    startDate = DateField('Start Date', validators=[Optional()])
    startTime = TimeField('Start Time', validators=[Optional()])
    day = SelectField('Day of the Week', choices=days)
    level = SelectField('Level', choices=levels)
    submit = SubmitField('Search')


class LessonForm(FlaskForm):
    name = StringField('Name')
    startDate = DateField('Start Date', render_kw={'placeholder': 'MM/DD/YYYY'})
    endDate = DateField('End Date', render_kw={'placeholder': 'MM/DD/YYYY'})
    startTime = TimeField('Start Time', render_kw={'placeholder': 'HH:MM'})
    endTime = TimeField('End Time', render_kw={'placeholder': 'HH:MM'})
    email = StringField('Contact Email')
    level = SelectField('Level', choices=levels[1:7])
    location = StringField('Location')
    desc = StringField('Add Description')
    cap = IntegerField('Max Enrollment')
    instructor = StringField('Instructor')
    submit = SubmitField('Create Lesson')
    day = SelectField('Day of the Week', choices=days)


class RegistrationForm(FlaskForm):
    fName = StringField('First Name of Participant', validators=[Optional()])
    lName = StringField('Last Name of Participant', validators=[Optional()])
    contactNum = StringField('Contact Phone Number (Optional)', render_kw={'placeholder': '123-456-7890'})
    contactEmail = StringField('Contact Email', validators=[Optional()])
    yourself = RadioField('Signing up yourself?', choices=[('value', 'Yes')], validators=[Optional()])
    submit = SubmitField('Register')


class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit Changes')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Choose another.')


class EditRegistrationForm(FlaskForm):
    contactNum = StringField('Contact Phone Number', render_kw={'placeholder': '123-456-7890'})
    contactEmail = StringField('Contact Email', validators=[Optional()])
    submit = SubmitField('Submit Changes')




