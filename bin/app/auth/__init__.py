"""Internal routing for config application"""
from flask import Blueprint
from .views import *

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
auth.add_url_rule('/login', view_func=login_view, methods=['GET', 'POST'])
auth.add_url_rule('/users', view_func=users_view, methods=['GET'])
auth.add_url_rule('/resetpasswd', view_func=resetpasswd_view, methods=['GET', 'POST'])
auth.add_url_rule('/user/delete', view_func=delete_user_view, methods=['POST'])
auth.add_url_rule('user/new', view_func=new_user_view, methods=['POST'])