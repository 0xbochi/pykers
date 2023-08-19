from http.client import NOT_FOUND
from flask import render_template, jsonify, request
import docker
from docker.errors import ImageNotFound


client = docker.from_env()

def volume_view():
    containers = client.containers.list(all=True)
    volume_data = []

    for container in containers:
        mounts = container.attrs['Mounts']
        for mount in mounts:
            volume_info = {
                "source": mount['Source'],
                "destination": mount['Destination'],
                "name": container.name,
                "active": container.status == "running",
                "id": container.id
            }
            volume_data.append(volume_info)

    return render_template('volumes.html', volumes=volume_data)
