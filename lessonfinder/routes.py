from flask import render_template, url_for, flash, redirect, request
from lessonfinder import app, db, user_manager
from lessonfinder.form import LoginForm, SearchForm, LessonForm, SignupForm, RegistrationForm, levels, UpdateLessonForm, UpdatePasswordForm, UpdateUsernameForm
from lessonfinder.models import User, Role, Lesson, Organization
# from flask_login import login_user, current_user, logout_user, login_required
from flask_user import current_user, login_required, roles_required
from sqlalchemy import or_


# helper table for many-to-many relationships
# currently not working
# classes = db.Table('classes', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'), primary_key=True))
# ****https://flask-user.readthedocs.io/en/latest/basic_app.html: can help with admin roles


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated and current_user.roles == 'user':
        return redirect(url_for('profile'))
    elif current_user.is_authenticated and current_user.roles == 'admin':
        return redirect(url_for('admin_profile'))
    form = SignupForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name="user").first()
        user = User(fName=form.fName.data, lName=form.lName.data, email=form.email.data, active=True, username=form.username.data,
                    password=user_manager.hash_password(form.password.data))
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('user.login'))
    return render_template('signup_page.html', title='Sign Up', form=form)


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


@app.route("/lesson_info/<int:lesson_id>")
@login_required
def lesson_info(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    return render_template('lesson_info.html', title="Information", lesson=lesson)


@app.route("/profile")
@login_required
def profile():
    role = current_user.roles
    role = role[0]
    if current_user.is_authenticated and role.name == 'admin':
        return redirect(url_for('admin_profile'))
    elif current_user.is_authenticated:
        lessons = current_user.lessons
    return render_template('profile.html', title="Profile", lessons=lessons)


@app.route('/update_username', methods=['GET', 'POST'])
@roles_required('user')
@login_required
def update_username():
    form = UpdateUsernameForm()
    user = current_user
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        flash(f'Success', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_username.html', title='Change Username', form=form)


@app.route("/update_lesson/<int:lesson_id>/", methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    form = UpdateLessonForm()
    if form.validate_on_submit():
        if form.cap.data and (lesson.users.count() > form.cap.data):
            flash(f'The number of users registered exceeds the maximum enrollment. You can\'t change it.', 'danger')
        else:
            # could be used to set a day of the week
            # day.strftime('%A')
            update_lesson_helper(form, lesson)
            flash(f'Lesson updated successfully.')
            return redirect(url_for('admin_profile'))
    return render_template('update_lesson.html', title='Edit Information', form=form, lesson=lesson)


def update_lesson_helper(form, lesson):
    if form.name.data:
        lesson.name = form.name.data
    if form.startDate.data:
        lesson.startDate = form.startDate.data
    if form.endDate.data:
        lesson.endDate = form.endDate.data
    if form.startTime.data:
        lesson.startTime = form.startTime.data
    if form.endTime.data:
        lesson.endTime = form.endTime.data
    if form.level.data:
        lesson.level = form.level.data
    if form.location.data:
        lesson.location = form.location.data
    if form.desc.data:
        lesson.desc = form.desc.data
    if form.cap.data:
        lesson.cap = form.cap
    if form.instructor.data:
        lesson.instructor = form.instructor.data
    db.session.commit()


@app.route("/admin_profile")
@roles_required('admin')
@login_required
def admin_profile():
    if current_user.is_authenticated:
        lessons = current_user.organizer
        org = current_user.organization
    return render_template('admin_profile.html', title="Admin Profile", lessons=lessons, org=org)


@app.route("/new_lesson/new", methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def new_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        user = current_user
        lesson = Lesson(name=form.name.data, startDate=form.startDate.data, endDate=form.endDate.data,
                        startTime=form.startTime.data, endTime=form.endTime.data,
                        contactEmail=user, level=form.level.data, location=form.location.data,
                        organization=user.organization.name, instructor=form.instructor.data,
                        cap=int(form.cap.data))
        user.organizer.append(lesson)
        db.session.add(lesson)
        db.session.commit()
        flash('The lesson has been created!', 'success')
        return redirect(url_for('admin_profile'))
    else:
        flash('Unsuccessful. Please check all fields.', 'danger')
    return render_template('create_lesson.html', title="New Lesson", form=form)


@app.route("/remove/<int:lesson_id>/delete", methods=['POST'])
@roles_required('admin')
@login_required
def remove(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('The lesson has been removed', 'success')
    return redirect(url_for('admin_profile'))


@app.route("/view_lesson/<int:lesson_id>", methods=['GET', 'POST'])
@roles_required('admin')
@login_required
def view_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    return render_template('view_lesson.html', title="Lesson Information", lesson=lesson)



