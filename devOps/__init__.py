from flask import Flask, render_template,make_response,redirect
import os
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from itsdangerous.url_safe import URLSafeSerializer
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_jwt_extended import (jwt_required,get_jwt, get_jwt_identity,
                                create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies,unset_access_cookies)


from datetime import timedelta
from flask_jwt_extended import JWTManager
import detect
from flask_github import GitHub

app = Flask(__name__)


app.config['GITHUB_CLIENT_ID'] = "Iv1.661bd3d1d057d682"
app.config['GITHUB_CLIENT_SECRET'] = "515a5f63bc2241f2497aec2fc860c81a311c2fdd"
# For GitHub Enterprise
app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'
github = GitHub(app)


app.config['JENKINS_USERNAME']='hela'
app.config['JENKINS_PASSWORD']='e1a2e673d87f4a7bbe5e6ad6051bfd88'
app.config['JENKINS_URL']='http://localhost:8080/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devOps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = '522e542ab915edba480119d0'
ts = URLSafeSerializer(app.config["SECRET_KEY"])

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['BASE_URL'] = 'http://127.0.0.1:5000'  #Running on localhost
app.config['JWT_SECRET_KEY'] = 'jkhjfeksqgbfozeLHFNUEHDb'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds = 1800)
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_CSRF_CHECK_FORM'] = False
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
jwt = JWTManager(app)

login_manager = LoginManager(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

print(detect.py2)
print(detect.py3)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # No auth header
    return redirect(app.config['BASE_URL'] + '/login', 302)

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    # Invalid Fresh/Non-Fresh Access token in auth header
    resp = make_response(redirect(app.config['BASE_URL'] + '/'))
    unset_jwt_cookies(resp)
    return resp, 302

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    # Expired auth header
    resp = make_response(redirect(app.config['BASE_URL'] + '/token/refresh'))
    unset_access_cookies(resp)
    return resp, 302


from devOps import routes
#from devOps.models import User





