from flask import Blueprint
from .views import index, get_containers

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')
home.add_url_rule('/', view_func=index)
home.add_url_rule('/api/containers', view_func=get_containers)
