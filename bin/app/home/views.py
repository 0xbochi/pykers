from flask import render_template, jsonify
import docker
from docker.errors import ImageNotFound


client = docker.from_env()

def index():
    return render_template('index.html')

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
