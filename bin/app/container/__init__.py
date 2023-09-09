from flask import Blueprint
from .views import *

container = Blueprint('container', __name__, template_folder='templates', static_folder='static')
container.add_url_rule('/<string:id>', view_func=details)
container.add_url_rule('/<string:id>/stop', view_func=stop, methods=['POST'])
container.add_url_rule('/<string:id>/start', view_func=start, methods=['POST'])
container.add_url_rule('/<string:id>/remove', view_func=remove, methods=['POST'])
container.add_url_rule('/<string:id>/details_api', view_func=details_api, methods=['GET'])
container.add_url_rule('/<string:id>/restart', view_func=restart, methods=['POST'])
container.add_url_rule('/<string:id>/logs', view_func=logs, methods=['GET'])
container.add_url_rule('/<string:id>/stats', view_func=stats, methods=['GET'])
container.add_url_rule('/<string:id>/exec', view_func=exec, methods=['POST'])
container.add_url_rule('/<string:id>/inspect', view_func=inspect, methods=['GET'])
container.add_url_rule('/<string:id>/copy', view_func=copy, methods=['POST'])
