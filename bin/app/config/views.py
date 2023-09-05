"""View of port application"""
from http.client import NOT_FOUND
from flask import render_template, jsonify, request
import docker
from docker.errors import ImageNotFound


client = docker.from_env()


def config_view() -> str:
    return render_template('config.html')
