from flask import render_template, url_for, flash, redirect
from lessonfinder import app
from lessonfinder.form import RegistrationForm, LoginForm, SearchForm
from lessonfinder.models import User, Admin, Instructor, Lesson

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


# helper table for many-to-many relationships
# currently not working
# classes = db.Table('classes', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'), primary_key=True))


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
