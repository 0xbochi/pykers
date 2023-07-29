from flask import Flask, redirect, url_for
from app.home import home
from app.container import container
from app.create import create

app = Flask(__name__)
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(container, url_prefix='/container')
app.register_blueprint(create, url_prefix='/create')


@app.route('/')
def root():
    return redirect(url_for('home.index'))



