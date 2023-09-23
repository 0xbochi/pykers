"""Internal routing for create application"""
from flask import Blueprint
from .views import *

create = Blueprint('create', __name__, template_folder='templates', static_folder='static')
create.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
create.add_url_rule('/check_image', view_func=check_image, methods=['POST'])
create.add_url_rule('/check_container_name', view_func=check_container_name, methods=['POST'])
