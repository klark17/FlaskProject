import logging
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from flask_user import UserManager, SQLAlchemyAdapter
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL'] = True
app.config['CSRF_ENABLED'] = True
app.config['USER_USER_SESSION_EXPIRATION'] = 720
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# USER_USER_SESSION_EXPIRATION = 3600 -- set session expiration
db = SQLAlchemy(app)


# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from lessonfinder.models import User
from lessonfinder.form import LoginForm

user_manager = UserManager(app, db, User)

from lessonfinder import routes




