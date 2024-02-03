#!/usr/bin/python3
"""Blueprint to return status"""
from flask import Blueprint

app_views = Blueprint('blue_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
