"""Main routing for the entire application"""
import yaml
from ipaddress import ip_network, ip_address
from flask import Flask, redirect, url_for, send_from_directory, abort, request
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

def get_allowed_ips():
    try:
        with open('app/config.yaml', 'r') as f:
            config_data = yaml.safe_load(f)
            return config_data.get('ALLOWED_IPS', [])
    except FileNotFoundError:
        print("File not found")
        return []

@app.route('/')
def root():
    return redirect(url_for('home.index'))

@app.route('/common/static/<path:filename>')
def common_static(filename):
    return send_from_directory('app/common/static', filename)

@app.before_request
def limit_remote_addr():
    ALLOWED_IPS = get_allowed_ips()
    try:
        user_ip = ip_address(request.remote_addr)
        if not any(user_ip in ip_network(ip, strict=False) for ip in ALLOWED_IPS):
            abort(403)
    except ValueError as e:
        print(f"IP error : {e}")
        abort(403)