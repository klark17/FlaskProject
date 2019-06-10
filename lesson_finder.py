from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
from form import RegistrationForm, LoginForm, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# helper table for many-to-many relationships
# currently not working
# classes = db.Table('classes', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'), primary_key=True))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50), nullable=False)
    lName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer)
    # name = db.relationship('Lesson', backref='registered', lazy=True)
    # lessons = db.relationship('Lesson', secondary=classes, backref='user', lazy=True)
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
    lessons = db.relationship('Lesson', backref='organizer', lazy=True)

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
    instructor = db.Column(db.String(50), db.ForeignKey('instructor.email'), nullable=False)
    contactEmail = db.Column(db.String(50), db.ForeignKey('admin.email'), nullable=False)
    # registered = db.relationship('User', backref='registered_users', lazy=True)
    # for many-to-many: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

    def __repr__(self):
        return f"Lesson('{self.startDate}', '{self.endDate}', '{self.level}', '{self.location}')"


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup_page.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_page.html', title='Login', form=form)


@app.route("/results")
def results():
    return render_template('search_results.html', title='Results')


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('results'))
    return render_template('search_lessons.html', title='Search', form=form)


@app.route("/profile")
def profile():
    # form = SearchForm()
    # if form.validate_on_submit():
    #     return render_modal("modal")
    return render_template('profile.html', title="Profile")


if __name__ == '__main__':
    app.run(debug=True)