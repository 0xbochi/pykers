"""Views for create application"""
from flask import render_template, request, jsonify
from docker import DockerClient
from docker.errors import NotFound, ImageNotFound, APIError

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
                return jsonify(
                    {'error': f"Failed to pull image {image}. Error: {str(e)}"}), 500

        env_vars_str = request.form.get('env_vars')
        env_vars = dict(item.split("=")
                        for item in env_vars_str.split(",")) if env_vars_str else None

        volumes_str = request.form.get('volumes')
        if volumes_str:
            volume_list = volumes_str.split(",")
            volumes = {
                item.split(":")[0]: {
                    'bind': item.split(":")[1],
                    'mode': 'rw'} for item in volume_list}
        else:
            volumes = None

        ports_str = request.form.get('ports')
        ports = dict(item.split(":")
                     for item in ports_str.split(",")) if ports_str else None

        links_str = request.form.get('links')
        links = [item for item in links_str.split(",")] if links_str else None

        mem_limit = request.form.get('mem_limit')
        name = request.form.get('name')
        initial_command = request.form.get('initial_command')

        try:
            container = client.containers.create(
                image,
                command=initial_command,
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
        except APIError as e:
            return jsonify({'error': str(e)}), 400

    return render_template('create.html', images=images)


def check_image():
    image_name = request.form.get('image_name')
    try:
        client.images.get(image_name)
        return jsonify({'status': 'success'})
    except ImageNotFound:
        try:
            client.images.pull(image_name)
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})



def check_container_name():
    container_name = request.form.get('container_name')
    try:
        DockerClient.from_env().containers.get(container_name)
        return jsonify({'status': 'error', 'message': 'Container name already exists.'})
    except NotFound:
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred: ' + str(e)})