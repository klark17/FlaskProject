from flask import render_template, url_for, flash, redirect, request
from lessonfinder import app, db
from lessonfinder.form import RegistrationForm, LoginForm, SearchForm, LessonForm
from lessonfinder.models import User, Admin, Instructor, Lesson
from flask_login import login_user, current_user, logout_user, login_required


# helper table for many-to-many relationships
# currently not working
# classes = db.Table('classes', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'), primary_key=True))


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fName=form.fName.data, lName=form.lName.data, email=form.email.data, age=form.age.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('signup_page.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_page.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))


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
@login_required
def profile():
    # form = SearchForm()
    # if form.validate_on_submit():
    #     return render_modal("modal")
    return render_template('profile.html', title="Profile")


@app.route("/new_lesson/new", methods=['GET', 'POST'])
@login_required
def new_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        flash('The lesson has been created!', 'success')
        return redirect(url_for('profile'))
    return render_template('create_lesson.html', title="New Lesson", form=form)


