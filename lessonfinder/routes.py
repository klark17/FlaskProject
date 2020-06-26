from flask import render_template, url_for, flash, redirect, request
from lessonfinder import app, db, user_manager
from lessonfinder.form import SearchForm, SignupForm, RegistrationForm, levels, \
    UpdateUsernameForm, EditRegistrationForm
from lessonfinder.models import User, Participant, Lesson
from flask_user import current_user, login_required, roles_required
from sqlalchemy import or_


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated and current_user.roles == 'user':
        return redirect(url_for('profile'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(active=True, fName=form.fName.data, lName=form.lName.data, email=form.email.data, birthday=form.birthday.data,
                    username=form.username.data, password=user_manager.hash_password(form.password.data))
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
                                      Lesson.startDate == form.startDate.data,
                                      Lesson.startTime == form.startTime.data,
                                      Lesson.day == form.day.data,
                                      Lesson.level == level_choice))
        if len(results.all()) == 0:
            flash('Your search did not yield any results. Please try again.', 'danger')
        else:
            return search_results(results)
    return render_template('search_lessons.html', title='Search', form=form)


@app.route('/register_yourself/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def register_yourself(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson in current_user.lessons:
        flash(f'You are already registered for this lesson. Please search for another one.', 'danger')
        return redirect('/search')
    else:
        current_user.lessons.append(lesson)
        db.session.commit()
        flash(f'You have successfully registered!', 'success')
    return redirect('/profile')


@app.route("/register/<int:lesson_id>", methods=['GET', 'POST'])
@login_required
def register(lesson_id):
    form = RegistrationForm()
    lesson = Lesson.query.get_or_404(lesson_id)
    if form.validate_on_submit():
        dependents = current_user.dependents
        dependent = Participant(fName=form.fName.data, lName=form.lName.data, contactNum=form.contactNum.data,
                                contactEmail=form.contactEmail.data)
        if not dependents:
            current_user.dependents.append(dependent)
            dependent.lessons.append(lesson)
            db.session.add(dependent)
            db.session.commit()
            flash(f'Your dependent has been registered!', 'success')
            return redirect(url_for('profile'))
        elif dependents:
            exists = False
            for dep in dependents:
                if dep.fName == dependent.fName and dep.lName == dependent.lName:
                    exists = True
                    existingDep = dep
                    break
            if exists:
                if lesson in existingDep.lessons:
                    flash(f'You\'re dependent is already registered for this lesson. Please search for another one.', 'danger')
                    return redirect('/search')
                else:
                    existingDep.lessons.append(lesson)
                    db.session.commit()
                    flash(f'Your dependent has been registered!', 'success')
                return redirect(url_for('profile'))
            else:
                current_user.dependents.append(dependent)
                dependent.lessons.append(lesson)
                db.session.add(dependent)
                db.session.commit()
                flash(f'Your dependent has been registered!', 'success')
                return redirect(url_for('profile'))
    return render_template('register.html', title='Register', form=form, lesson=lesson)


@app.route("/unregister/<int:lesson_id>/delete", methods=['POST'])
@login_required
def unregister_user(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    for user in lesson.selfParticipant:
        if current_user.id == user.id:
            lesson.selfParticipant.remove(user)
            db.session.commit()
            flash(f'You have successfully unregistered from ' + lesson.name, 'success')
            break
        else:
            continue
    return redirect(url_for('profile'))


@app.route("/unregister_dep/<int:lesson_id>/delete/<int:dep_id>", methods=['POST'])
@login_required
def unregister_dep(lesson_id, dep_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    dependent = Participant.query.get_or_404(dep_id)
    dependent.lessons.remove(lesson)
    db.session.commit()
    return redirect(url_for('profile'))


@app.route("/dep_lesson_info/<int:lesson_id>/<int:dep_id>")
@login_required
def dep_lesson_info(lesson_id, dep_id):
    lesson = Lesson.query.get(lesson_id)
    dependent = Participant.query.get(dep_id)
    return render_template('dep_lesson_info.html', title="Information", lesson=lesson, dependent=dependent)


@app.route("/lesson_info/<int:lesson_id>")
@login_required
def lesson_info(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    return render_template('lesson_info.html', title="Information", lesson=lesson)


@app.route("/profile")
@login_required
def profile():
    if current_user.is_authenticated:
        lessons = current_user.lessons
        dependents = current_user.dependents
        depLessons = []
        for dependent in dependents:
            for lesson in dependent.lessons:
                depLessons.append(lesson)
        return render_template('profile.html', title="Profile",
                               lessons=lessons, dependents=dependents, depLessons=depLessons)


@app.route("/edit_registration/<int:dep_id>", methods=['GET', 'POST'])
@login_required
def edit_registration(dep_id):
    form = EditRegistrationForm()
    dep = Participant.query.get_or_404(dep_id)
    if form.validate_on_submit():
        update_registration_helper(form, dep)
        flash(f'Registration updated successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_registration.html', title="Edit", form=form, dep=dep)


def update_registration_helper(form, dep):
    if form.contactNum.data:
        dep.contactNum = form.contactNum.data
    if form.contactEmail.data:
        dep.contactEmail = form.contactEmail.data
    db.session.commit()


@app.route('/update_username', methods=['GET', 'POST'])
@login_required
def update_username():
    form = UpdateUsernameForm()
    user = current_user
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        flash(f'Username was successfully changed!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_username.html', title='Change Username', form=form)


@app.route('/remove_dep/<int:dep_id>', methods=['POST'])
@login_required
def remove_dep(dep_id):
    dependent = Participant.query.get_or_404(dep_id)
    db.session.delete(dependent)
    db.session.commit()
    flash(f'Dependent was successfully deleted.', 'success')
    return redirect(url_for('profile'))
