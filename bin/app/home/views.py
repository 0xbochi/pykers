"""View of home application"""
from flask import render_template, jsonify
import docker
from docker.errors import ImageNotFound


client = docker.from_env()


def index() -> str:
    """
    Retrieve a list of images and containers, and render them in the 'index.html' template.

    This function fetches the latest images and a limited number of containers.
    It then extracts the volumes and ports associated with these containers.

    Returns:
        str: Rendered 'index.html' template with details of images and containers.
    """
    images = client.images.list()
    last_images = images[-5:] if len(images) > 5 else images

    containers = client.containers.list(all=False, limit=3)
    container_ports = []
    container_volumes = []

    for container in containers:
        mounts = container.attrs['Mounts']
        for mount in mounts:
            container_volumes.append(
                f"{mount['Source']}:{mount['Destination']}")
            if len(container_volumes) == 4:
                break

        ports = container.attrs['NetworkSettings']['Ports']
        for k, v in ports.items():
            if v and isinstance(v, list) and len(v) > 0 and 'HostPort' in v[0]:
                container_ports.append(f"{v[0]['HostPort']}:{k.split('/')[0]}")
            if len(container_ports) == 4:
                break

        if len(container_ports) == 4 and len(container_volumes) == 4:
            break

    return render_template(
        'index.html',
        image_count=len(images),
        last_images=last_images,
        container_ports=container_ports,
        container_volumes=container_volumes
    )


def get_containers() -> dict:
    """
    Retrieve a list of all containers and their associated details.

    This function fetches all containers and extracts their ID, name, status,
    and associated image tag. If an image tag is not found, it defaults to "No image".

    Returns:
        dict: A JSON representation of the list of containers and their details.
    """
    containers = client.containers.list(all=True)
    containers_data = []

    for c in containers:
        try:
            image_tag = c.image.tags[0] if c.image.tags else "No image"
        except ImageNotFound:
            image_tag = "No image"

        containers_data.append({
            'id': c.id,
            'name': c.name,
            'status': c.status,
            'image': image_tag
        })

    return jsonify(containers_data)
