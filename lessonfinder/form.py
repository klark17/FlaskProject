from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, \
    DateTimeField, IntegerField, DateField, TimeField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from wtforms_components import TimeField, DateField, DateRange
from lessonfinder.models import User
from datetime import date
from dateutil.relativedelta import relativedelta

levels = [('None', 'None'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')]
days = [('None', 'None'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                                                  ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                                  ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]


class SignupForm(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired()])
    lName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birthday = DateField('Birthday', validators=[DataRequired(), DateRange(max=date.today()-relativedelta(years=18))])
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


class SearchForm(FlaskForm):
    location = StringField('Location')
    startDate = DateField('Start Date', validators=[Optional()])
    startTime = TimeField('Start Time', validators=[Optional()])
    day = SelectField('Day of the Week', choices=days)
    level = SelectField('Level', choices=levels)
    submit = SubmitField('Search')


class RegistrationForm(FlaskForm):
    fName = StringField('First Name of Participant', validators=[DataRequired()])
    lName = StringField('Last Name of Participant', validators=[DataRequired()])
    contactNum = StringField('Contact Phone Number (Optional)', validators=[Optional()], render_kw={'placeholder': '123-456-7890'})
    contactEmail = StringField('Contact Email', validators=[DataRequired()])
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
