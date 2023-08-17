from flask import render_template, jsonify
import docker
from docker.errors import ImageNotFound


client = docker.from_env()

def index():
  
    images = client.images.list()
    last_images = images[-5:] if len(images) > 5 else images

    containers = client.containers.list(all=False, limit=3)
    container_ports = []
    container_volumes = []
    for container in containers:
        mounts = container.attrs['Mounts']
        for mount in mounts:
            container_volumes.append(f"{mount['Source']}:{mount['Destination']}")

        ports = container.attrs['NetworkSettings']['Ports']
        for k, v in ports.items():
            if v and isinstance(v, list) and len(v) > 0 and 'HostPort' in v[0]:
                container_ports.append(f"{v[0]['HostPort']}:{k.split('/')[0]}")



    return render_template('index.html', image_count=len(images), last_images=last_images, container_ports=container_ports, container_volumes=container_volumes)

def get_containers():
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
