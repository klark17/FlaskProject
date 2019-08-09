from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_components import TimeField, DateField
from lessonfinder.models import User


levels = [('text', 'None'), ('int', '1'), ('int', '2'), ('int', '3'), ('int', '4'), ('int', '5'), ('int', '6')]


class SignupForm(FlaskForm):
	fName = StringField('First Name', validators=[DataRequired()])
	lName = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	age = IntegerField('Age (Must be 18 years old)', validators=[DataRequired()])
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
	startDate = DateField('Start Date (*Required)')
	startTime = TimeField('Start Time (*Required)')
	level = SelectField('Level', choices=levels)
	submit = SubmitField('Search')


class LessonForm(FlaskForm):
	name = StringField('Name')
	# type = StringField('Type')
	startDate = DateField('Start Date', render_kw={'placeholder': 'MM/DD/YYYY'})
	endDate = DateField('End Date', render_kw={'placeholder': 'MM/DD/YYYY'})
	startTime = TimeField('Start Time', render_kw={'placeholder': 'HH:MM'})
	endTime = TimeField('End Time', render_kw={'placeholder': 'HH:MM'})
	email = StringField('Contact Email')
	level = SelectField('Level', choices=levels[1:7])
	location = StringField('Location')
	desc = StringField('Add Description')
	instructor = StringField('Instructor')
	submit = SubmitField('Create Lesson')
	# possibly going to remove completely
	# not currently in the Lesson model
	# day = SelectField('Day of the Week', choices=[('text', 'Monday'), ('text', 'Tuesday'), ('text', 'Wednesday'),
	# 									('text', 'Thursday'), ('text', 'Friday'), ('text', 'Saturday'),
	# 									('text', 'Sunday')])


class OrganizationForm(FlaskForm):
	name = StringField('Name of Organization')
	address = StringField('Address')
	town = StringField('Town/City')
	state = StringField('State')


class RegistrationForm(FlaskForm):
	name = StringField('Name of Participant')
	contactEmail = StringField('Contact Email')
	submit = SubmitField('Register')



