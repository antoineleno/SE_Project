#!/usr/bin/python3
"""
APP module
"""

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
#from models import storage
from flask_login import current_user
from auth.forms import SignInForm, SignUpForm, ForgotPasswordForm
#from models.models import User
from datetime import datetime


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})
app.secret_key = "a2cf8cf6ad37b0d8eb2b51846aee0e34"




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app_views_auth.login_view'





@login_manager.user_loader
def load_user(id):
    """Load current user session"""
    return storage.get_object(User, id=id)


@app.teardown_appcontext
def teardown_db(exception):
    """Close everytime the opened session"""
    try:
        storage.close()
    except Exception as e:
        print("this is the error from tear down {}".format(e))
        pass

if __name__ == "__main__":
    app.run(debug=True)
