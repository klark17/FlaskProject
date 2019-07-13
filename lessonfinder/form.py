from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lessonfinder.models import User


class RegistrationForm(FlaskForm):
	fName = StringField('First Name', validators=[DataRequired()])
	lName = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	age = IntegerField('Age (Must be 18 years old)', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data)
		if user:
			raise ValidationError('Username is taken. Choose another.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data)
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
	type = StringField('Type')
	level = SelectField('Level', choices=[('text', 'Beginner/Levels 1-2'),
										  ('text', 'Intermediate/Levels 3-5'), ('text', 'Advanced/Levels 6+')])
	time = DateTimeField('Start Date and Time')
	submit = SubmitField('Search')


class LessonForm(FlaskForm):
	name = StringField('Name')
	type = StringField('Type')
	startMonth = SelectField('Start Month', choices=[('text', 'January'), ('text', 'February'), ('text', 'March'),
							('text', 'April'), ('text', 'May'), ('text', 'June'), ('text', 'July'), ('text', 'August'),
							('text', 'September'), ('text', 'October'), ('text', 'November'), ('text', 'December')])
	startDate = IntegerField('Start Date')
	endMonth = SelectField('Start Date', choices=[('text', 'January'), ('text', 'February'), ('text', 'March'),
							('text', 'April'), ('text', 'May'), ('text', 'June'), ('text', 'July'), ('text', 'August'),
							('text', 'September'), ('text', 'October'), ('text', 'November'), ('text', 'December')])
	endDate = IntegerField('End Date')
	startTime = StringField('Start Time') #DateTimeField('Start Time')
	endTime = StringField('End Time') #DateTimeField('End Time')
	day = SelectField('Level', choices=[('text', 'Monday'), ('text', 'Tuesday'), ('text', 'Wednesday'),
										('text', 'Thursday'), ('text', 'Friday'), ('text', 'Saturday'),
										('text', 'Sunday')])
	email = StringField('Contact Email')
	level = SelectField('Level', choices=[('text', 'Beginner/Levels 1-2'),
										('text', 'Intermediate/Levels 3-5'), ('text', 'Advanced/Levels 6+')])
	location = StringField('Location')
	organization = StringField('Organization')
	instructor = StringField('Instructor')
	submit = SubmitField('Create Lesson')


