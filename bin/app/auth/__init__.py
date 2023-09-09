"""Internal routing for config application"""
from flask import Blueprint
from .views import *

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
auth.add_url_rule('/login', view_func=login_view, methods=['GET', 'POST'])