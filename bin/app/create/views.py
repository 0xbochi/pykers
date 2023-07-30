from flask import render_template, request, jsonify, redirect, url_for
from docker import DockerClient
from docker.errors import NotFound

client = DockerClient.from_env()


def index():
    images = [img.tags[0] for img in client.images.list() if img.tags]
    if request.method == 'POST':

        image = request.form.get('image')

        env_vars_str = request.form.get('env_vars')
        env_vars = dict(item.split("=") for item in env_vars_str.split(",")) if env_vars_str else None


        volumes_str = request.form.get('volumes')
        volumes = dict(item.split(":") for item in volumes_str.split(",")) if volumes_str else None


        ports_str = request.form.get('ports')
        ports = dict(item.split(":") for item in ports_str.split(",")) if ports_str else None


        links_str = request.form.get('links')
        links = [item for item in links_str.split(",")] if links_str else None

        mem_limit = request.form.get('mem_limit')
        name = request.form.get('name')

        print("image", image)


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

        return redirect(url_for('container.details', id=container.id))

    return render_template('create.html', images=images)



