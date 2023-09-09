"""Main routing for the entire application"""
import yaml
from ipaddress import ip_network, ip_address
from flask import Flask, redirect, url_for, send_from_directory, abort, request, Response
from app.home import home
from app.container import container
from app.create import create
from app.image import image
from app.port import port
from app.volume import volume
from app.config import config

app = Flask(__name__, template_folder='templates', static_folder='static')
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(container, url_prefix='/container')
app.register_blueprint(create, url_prefix='/create')
app.register_blueprint(image, url_prefix='/image')
app.register_blueprint(port, url_prefix='/port')
app.register_blueprint(volume, url_prefix='/volume')
app.register_blueprint(config, url_prefix='/config')

def load_config():
    try:
        with open('app/config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("File not found")
        return {'ALLOWED_IPS': [], 'AUTH_REQUIRED': False, 'USERS': {}}

@app.route('/')
def root():
    return redirect(url_for('home.index'))

@app.route('/common/static/<path:filename>')
def common_static(filename):
    return send_from_directory('app/common/static', filename)

@app.before_request
def before_request():
    config = load_config()

    # IP restriction
    try:
        user_ip = ip_address(request.remote_addr)
        if not any(user_ip in ip_network(ip, strict=False) for ip in config['ALLOWED_IPS']):
            abort(403)
    except ValueError as e:
        print(f"IP error : {e}")
        abort(403)

    # Authentication
    if config['AUTH_REQUIRED']:
        auth = request.authorization
        if auth and auth.username in config['USERS'] and config['USERS'][auth.username] == auth.password:
            return
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
