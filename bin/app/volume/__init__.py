"""Internal routing for create application"""
from flask import Blueprint
from .views import volume_view

volume = Blueprint(
    'volume',
    __name__,
    template_folder='templates',
    static_folder='static')
volume.add_url_rule('/', view_func=volume_view, methods=['GET', 'POST'])
