#!/usr/bin/python3
"""
AUTH module
"""

from flask import Blueprint, render_template, session
from flask import redirect, url_for, flash, request, jsonify
from models import storage
from models.models import User
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from .forms import SignInForm, SignUpForm, ForgotPasswordForm
from auth import app_views_auth


import datetime
import os
from operator import attrgetter


auth = Blueprint('auth', __name__)

@app_views_auth.route("/")
def home():
    """SignIn"""
    return "This is auth blueprint"
