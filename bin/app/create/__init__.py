from flask import Blueprint
from .views import *

create = Blueprint('create', __name__, template_folder='templates', static_folder='static')
create.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
