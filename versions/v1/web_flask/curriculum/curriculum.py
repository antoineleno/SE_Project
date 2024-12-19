#!/usr/bin/python3
"""
AUTH module
"""

from flask import Blueprint, render_template, session
from flask import redirect, url_for, flash, request, jsonify
from models import storage
from models.models import User
from curriculum import app_views_curriculum


import datetime
import os
from operator import attrgetter


curriculum = Blueprint('curriculum', __name__)

@app_views_curriculum.route("/")
def home():
    """SignIn"""
    return "This is from curriculum"
