"""Main routing for the entire application"""
from flask import Flask, redirect, url_for
from app.home import home
from app.container import container
from app.create import create
from app.image import image
from app.port import port

app = Flask(__name__)
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(container, url_prefix='/container')
app.register_blueprint(create, url_prefix='/create')
app.register_blueprint(image, url_prefix='/image')
app.register_blueprint(port, url_prefix='/port')


@app.route('/')
def root():
    return redirect(url_for('home.index'))