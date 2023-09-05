"""Internal routing for config application"""
from flask import Blueprint
from .views import config_view

config = Blueprint('config', __name__, template_folder='templates', static_folder='static')
config.add_url_rule('/', view_func=config_view, methods=['GET', 'POST'])