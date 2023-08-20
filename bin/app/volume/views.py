"""View of volume application"""
from http.client import NOT_FOUND
from flask import render_template, jsonify, request
import docker
from docker.errors import ImageNotFound


client = docker.from_env()


def volume_view() -> str:
    """
    Retrieve and display details of volumes associated with Docker containers.

    This function fetches a list of all Docker containers and extracts the volume details
    associated with each container. The details include the source path, destination path
    inside the container, container name, container status (active or not), and container ID.
    The extracted volume details are then displayed in the 'volumes.html' template.

    Returns:
        str: Rendered 'volumes.html' template with volume details.
    """
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
