"""Internal routing for create application"""
from flask import Blueprint
from .views import image_view, delete_image, pull_image, delete_containers_for_image

image = Blueprint('image', __name__, template_folder='templates', static_folder='static')
image.add_url_rule('/', view_func=image_view, methods=['GET', 'POST'])
image.add_url_rule('/pull', view_func=pull_image, methods=['POST'])
image.add_url_rule('/delete', view_func=delete_image, methods=['POST'])
image.add_url_rule('/delete-containers', view_func=delete_containers_for_image, methods=['POST'])
image.add_url_rule('/pull_image', view_func=pull_image, methods=['GET', 'POST'])
