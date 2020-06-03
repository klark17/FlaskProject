from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['USER_ENABLE_EMAIL'] = False
app.config['USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL'] = True
app.config['CSRF_ENABLED'] = True
app.config['USER_USER_SESSION_EXPIRATION'] = 720
db = SQLAlchemy(app)

from lessonfinder.models import User

user_manager = UserManager(app, db, User)

from lessonfinder import routes




