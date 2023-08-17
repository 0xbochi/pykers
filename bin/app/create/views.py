"""Views for create application"""
from flask import render_template, request, jsonify, redirect, url_for
from docker import DockerClient
from docker.errors import NotFound, ImageNotFound

client = DockerClient.from_env()

def index() -> dict:
    """Retrieves container informations.

    GET : Send all container information
    POST : Apply the creations of container
    """

    images = [img.tags[0] for img in client.images.list() if img.tags] 
    if request.method == 'POST':

        image = request.form.get('image')

        try:
            client.images.get(image)
        except ImageNotFound:
            try:
                client.images.pull(image)
            except Exception as e:
                return jsonify({'error': f"Failed to pull image {image}. Error: {str(e)}"}), 500

        env_vars_str = request.form.get('env_vars')
        env_vars = dict(item.split("=") for item in env_vars_str.split(",")) if env_vars_str else None

        volumes_str = request.form.get('volumes')
        if volumes_str:
            volume_list = volumes_str.split(",")
            volumes = {item.split(":")[0]: {'bind': item.split(":")[1], 'mode': 'rw'} for item in volume_list}
        else:
            volumes = None

        ports_str = request.form.get('ports')
        ports = dict(item.split(":") for item in ports_str.split(",")) if ports_str else None

        links_str = request.form.get('links')
        links = [item for item in links_str.split(",")] if links_str else None

        mem_limit = request.form.get('mem_limit')
        name = request.form.get('name')

        print(volumes)

        container = client.containers.create(
            image,
            environment=env_vars,
            volumes=volumes,
            ports=ports,
            links=links,
            mem_limit=mem_limit,
            name=name,
            detach=True
        )

        container.start()

        return jsonify({'id': container.id}), 200

    return render_template('create.html', images=images)