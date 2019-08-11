from flask import render_template, url_for, flash, redirect, request
from lessonfinder import app, db
from lessonfinder.form import LoginForm, SearchForm, LessonForm, OrganizationForm, SignupForm, RegistrationForm, levels
from lessonfinder.models import User, Admin, Lesson, Organization
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
from datetime import date, time


# helper table for many-to-many relationships
# currently not working
# classes = db.Table('classes', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'), primary_key=True))
# ****https://flask-user.readthedocs.io/en/latest/basic_app.html: can help with admin roles


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


# TODO: validate that the user is above the age of 18
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = SignupForm()
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
        if db.session.query(User.id).filter_by(username=form.username.data).scalar():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('You have been logged in!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('profile'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        elif db.session.query(Admin.id).filter_by(username=form.username.data).scalar():
            admin = Admin.query.filter_by(username=form.username.data).first()
            if admin and admin.password == form.password.data:
                login_user(admin, remember=form.remember.data)
                org = admin.organization
                flash('You have been logged in as an administrator!', 'success')
                return render_template('admin_profile.html', name=org.name, lessons=admin.lessons)
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_page.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))


@app.route("/results")
def search_results(results):
    return render_template('search_results.html', title='Results', results=results)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    level_choice = dict(levels).get(form.level.data)
    if form.validate_on_submit():
        results = Lesson.query.filter(or_(Lesson.location == form.location.data,
                                      Lesson.organization == form.organization.data,
                                      Lesson.startDate == form.startDate.data,
                                      Lesson.startTime == form.startTime.data,
                                      Lesson.level == level_choice))
        if len(results.all()) == 0:
            flash('Your search did not yield any results. Please try again.', 'danger')
        else:
            return search_results(results)
    return render_template('search_lessons.html', title='Search', form=form)


@app.route("/register/<int:lesson_id>", methods=['GET', 'POST'])
@login_required
def register(lesson_id):
    form = RegistrationForm()
    lesson = Lesson.query.get_or_404(lesson_id)
    if form.validate_on_submit():
        current_user.lessons.append(lesson)
        db.session.commit()
        flash(f'You have been registered!', 'success')
        return redirect(url_for('profile'))
    return render_template('register.html', title='Register', form=form, lesson=lesson)


# TODO: edit this so it is more efficient
# related to reading AppenderBaseQuery
@app.route("/unregister/<int:lesson_id>/delete", methods=['POST'])
@login_required
def unregister(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    for user in lesson.users:
        if current_user.id == user.id:
            lesson.users.remove(user)
            db.session.commit()
            flash('You have unregistered from the lesson.', 'success')
            break
        else:
            continue
    return redirect(url_for('profile'))


@app.route("/edit/<int:lesson_id>")
@login_required
def edit(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    return render_template('edit.html', title="Information", lesson=lesson)


@app.route("/profile")
@login_required
def profile():
    if current_user.is_authenticated:
        lessons = current_user.lessons
    return render_template('profile.html', title="Profile", lessons=lessons)


@app.route("/admin_profile")
@login_required
def admin_profile():
    if current_user.is_authenticated:
        lessons = current_user.lessons
    return render_template('admin_profile.html', title="Admin Profile", lessons=lessons)


@app.route("/new_lesson/new", methods=['GET', 'POST'])
@login_required
def new_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        admin = Admin.query.first()
        lesson = Lesson(name=form.name.data, startDate=form.startDate.data, endDate=form.endDate.data,
                        startTime=form.startTime.data, endTime=form.endTime.data,
                        contactEmail=admin, level=form.level.data, location=form.location.data,
                        organization=admin.organization.name, instructor=form.instructor.data)
        admin.lessons.append(lesson)
        db.session.add(lesson)
        db.session.commit()
        flash('The lesson has been created!', 'success')
        return redirect(url_for('admin_profile'))
    # else:
    #     flash('Unsuccessful. Please check all fields.', 'danger')
    return render_template('create_lesson.html', title="New Lesson", form=form)


@app.route("/remove/<int:lesson_id>/delete", methods=['POST'])
@login_required
def remove(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('The lesson has been removed', 'success')
    return redirect(url_for('admin_profile'))


@app.route("/organization/<int:lesson_id>", methods=['GET', 'POST'])
@login_required
def view_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    return render_template('delete_lesson.html', title="Lesson Information", lesson=lesson)


#possibly help with determining if admin is associated with an organization
#if the user is not associated with an org. then it will make the add org button available
#if associated it will display the name of the organization in the admin profile
#db.session.query(Admin).filter(Admin.id == Organization.adminId).filter(Admin.name == 'dilbert')


