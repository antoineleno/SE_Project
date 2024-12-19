#!/usr/bin/python3
"""
AUTH module
"""

from flask import Blueprint, render_template, session
from flask import redirect, url_for, flash, request, jsonify
from models import storage
from models.models import User
from home import app_views_home


import datetime
import os
from operator import attrgetter


home = Blueprint('home', __name__)

@app_views_home.route("/")
def home():
    """SignIn"""
    return "This is from home"
