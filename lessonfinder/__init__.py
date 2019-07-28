from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from lessonfinder import routes

# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from lessonfinder.models import User, Lesson
#
#
# admin = Admin(app, name='microblog', template_mode='bootstrap3')
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Lesson, db.session))

# class LessonFinderModelView(ModelView):
#
#     def is_accessible(self):
#         return login.current_user.is_authenticated
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login', next=request.url))



