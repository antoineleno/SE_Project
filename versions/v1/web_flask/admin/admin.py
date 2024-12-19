#!/usr/bin/python3
"""
AUTH module
"""

from flask import Blueprint, render_template, session
from flask import redirect, url_for, flash, request, jsonify
from models import storage
from models.models import User
from admin import app_views_admin


import datetime
import os
from operator import attrgetter


admin = Blueprint('admin', __name__)

@app_views_admin.route("/")
def home():
    """SignIn"""
    return "This is from admin"
