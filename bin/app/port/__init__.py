"""Internal routing for create application"""
from flask import Blueprint
from .views import port_view

port = Blueprint('port', __name__, template_folder='templates', static_folder='static')
port.add_url_rule('/', view_func=port_view, methods=['GET', 'POST'])
