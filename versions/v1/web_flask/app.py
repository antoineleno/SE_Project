#!/usr/bin/python3
"""
APP module
"""

from flask import Flask
from auth import app_views_auth
from wishlist import app_views_wishlist
from home import app_views_home
from wishlist import app_views_sell
from wishlist import app_views_rent
from auth import app_views_message
from flask_cors import CORS
from flask_login import LoginManager
from models import storage
from models.user import User
from models.message import Message, RoomParticipants
from flask_login import current_user
from auth.forms import SignInForm, SignUpForm, ForgotPasswordForm
import os
from datetime import datetime


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})
app.secret_key = "a2cf8cf6ad37b0d8eb2b51846aee0e34"


app.register_blueprint(app_views_auth)
app.register_blueprint(app_views_wishlist)
app.register_blueprint(app_views_rent)
app.register_blueprint(app_views_sell)
app.register_blueprint(app_views_message)
app.register_blueprint(app_views_home)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app_views_auth.login_view'


@app.context_processor
def inject_user():
    """Inject all base variables"""
    unread_message = 0
    admin_phone_number = ""
    admin_email = ""
    admin_object = storage.get_object(User, user_type="Admin")
    if admin_object is not None:
        admin_phone_number = admin_object.phone_number
        admin_email = admin_object.email

    if current_user.is_authenticated:
        user_id = current_user.id
        user = storage.get_object(User, id=user_id)
        all_user_room = user.roomparticipants
        all_ids = []
        for u_room in all_user_room:
            all_ids.append(u_room.room_id)

        for u_room_id in all_ids:
            message_count = storage.get_object(
                cls=Message,
                count=True,
                room_id=u_room_id,
                user_id=user_id,
                read_status=False
                )
            print(message_count)
            unread_message += message_count

    profile_path = "user.avif"
    if current_user.is_authenticated:
        file_names = os.listdir("auth/static/img/")
        extensions = [".png", ".jpg", ".jpeg", ".gif"]
        matching_files = [
            f for f in file_names
            if f.startswith(str(current_user.id)) and
            any(f.endswith(ext) for ext in extensions)
        ]

        if matching_files:
            profile_path = matching_files[0]

    return {
        'user': current_user,
        'profile_path': profile_path,
        'sign_in_form': SignInForm(),
        'sign_up_form': SignUpForm(),
        'unread_message': unread_message,
        'admin_phone_number': admin_phone_number,
        'admin_email': admin_email,
        'forgot_password_form': ForgotPasswordForm()
    }


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
